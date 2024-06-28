#
# Index actions.
#

import ast

from lib.shared.node_util import to_src_without_children
from lib.shared.utils import get_parent_module_name

from .index_collection import (
    DependencyEntry,
    DependencyCollection,
    ConstantEntry,
    ConstantCollection,
    SSA_Block,
    SSA_Collection,
    SSA_Dep,
)


def index_dependency(flattened_cfg) -> DependencyCollection:
    """
    Index the dependency of each node in the flattened CFG.
    It only indicate which dependency the line has, but not
    the exact dependencies, which is recorded in the SSA.
    """
    deps = DependencyCollection()

    # get all blocks in CFG
    blocks = []
    for _, cfg in flattened_cfg.items():
        blocks += cfg.get_all_blocks()
    blocks_dict = {block.id: block for block in blocks}

    for block in blocks_dict.values():
        for index, node in enumerate(block.statements):
            src_node = to_src_without_children(node)
            deps.add(DependencyEntry(src_node, block.id, index))

    return deps


def index_constant(const_dict) -> ConstantCollection:
    """
    Index all constants of the SSA
    """
    consts = ConstantCollection()

    for name, value in const_dict.items():
        func_name = name
        for entry, node in value.items():
            if node is None:
                src_node = None
            else:
                src_node = to_src_without_children(node)
            consts.add(ConstantEntry(func_name + "." + entry[0], entry[1], src_node))

    return consts


def is_unresolved(id_set):
    return (id_set is None) or (len(id_set) == 0)


def index_ssa(ssa_results) -> SSA_Collection:
    """
    Index all SSA results, including blocks and dependencies.
    """
    contex = SSA_Collection()

    # {
    #   1: [{}, {}, {}, {'c': {0}, 'a': {0}}],
    #   2: ...
    # }
    for module_name, module in ssa_results.items():
        for block_id, block_result in module.items():
            block = SSA_Block()
            for block_entry in block_result:
                dep = SSA_Dep()
                for ident, id_set in block_entry.items():
                    # do not add empty dependency
                    # some dependencies are not resolved, and marked 'set()'
                    if is_unresolved(id_set):
                        id_list = None
                    else:
                        id_list = list(id_set)
                    dep.add(module_name + "." + ident, id_list)
                block.add(dep)
            contex.add(block_id, block)
    return contex


def _add_func_params_to_const_dict(const_dict, mod_name, func_node):
    """
    Add all params of a function to const_dict. It will make the subscript 0
    as params are bound to be the first variables.
    Also, it will return a list of params to make later use easier.
    """
    func_params = []
    const_block_name = mod_name + "." + func_node.name
    if const_block_name not in const_dict:
        const_dict[const_block_name] = {}
    const_block = const_dict[const_block_name]
    for arg in func_node.args.args:
        # There might be some problems if we use arg, which indeed should be used.
        # However, we can use func_node to avoid this, though not exactly the same.
        const_block[(arg.arg, 0)] = func_node
        # const_block[(arg.arg, 0)] = arg
        func_params.append(arg.arg)

    return const_block_name, func_params


def _mend_func_params(flattened_cfg, ssa_results, const_dict):
    """
    Since parameter information is missing in Scalpel SSA, we have to manually
    add these parameters to const_dict, and resolve the dependency in SSA.
    """
    func_param_dict = {}

    # add all parameters as constants with subscript 0
    for mod, cfg in flattened_cfg.items():
        for block in cfg.get_all_blocks():
            for node in block.statements:
                if isinstance(node, ast.FunctionDef):
                    name, params = _add_func_params_to_const_dict(const_dict, mod, node)
                    func_param_dict[name] = params

    for module_name, module in ssa_results.items():
        for _, block_result in module.items():
            for block_entry in block_result:
                for ident, id_set in block_entry.items():
                    if is_unresolved(id_set):
                        if ident in func_param_dict.get(module_name, []):
                            block_entry[ident] = {0}


def _try_find_outer_variable(flattened_cfg, const_dict, module_name, ident):
    """
    Recursively find the outer variable in the module.
    """
    if module_name == "":
        return None, None
    if module_name not in const_dict:
        return None, None

    const_block = const_dict[module_name]
    for k, v in const_block:
        if k == ident:
            return module_name, v
    return _try_find_outer_variable(
        flattened_cfg, const_dict, get_parent_module_name(module_name), ident
    )


def _mend_outer_variable(flattened_cfg, ssa_results, const_dict):
    """
    Mend outer variable dependency in SSA.
    By default, Scalpel cannot resolve variable declared in outer scope,
    however, it does generate the outer variable. So we have to manually
    add these dependencies.
    """
    for module_name, module in ssa_results.items():
        for _, block_result in module.items():
            for block_entry in block_result:
                for ident, id_set in block_entry.items():
                    if is_unresolved(id_set):
                        outer_module, outer_id = _try_find_outer_variable(
                            flattened_cfg, const_dict, module_name, ident
                        )
                        if outer_module is not None:
                            block_entry[ident] = {outer_id}


def mend_ssa(flattened_cfg, ssa_results, const_dict):
    _mend_func_params(flattened_cfg, ssa_results, const_dict)
    _mend_outer_variable(flattened_cfg, ssa_results, const_dict)
