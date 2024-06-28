from .index_collection import (
    ConstantCollection,
    ConstantEntry,
    DependencyCollection,
    DependencyEntry,
    SSA_Collection,
    SSA_Dep,
)
from scalpel.SSA.const import SSA
from scalpel.cfg import CFGBuilder
from lib.shared.logger import logger


def build_flattened_cfg(source_code):
    """
    Build flattened CFG from source code.
    """
    flattened_cfg = CFGBuilder().build_from_src("main", source_code, flattened=True)
    return flattened_cfg


def _compute_flattened_SSA(ssa: SSA, flattened_cfg):
    ssa_results = {}
    const_dict = {}
    for key in flattened_cfg:
        ssa_results[key], const_dict[key] = ssa.compute_SSA(flattened_cfg[key])
    return ssa_results, const_dict


def build_ssa(flattened_cfg):
    """
    Build SSA from flattened CFG.
    """
    m_ssa = SSA()  # forget about this stupid name
    ssa_results, const_dict = _compute_flattened_SSA(m_ssa, flattened_cfg)
    return ssa_results, const_dict


def build_dependencies(
    deps_collection: DependencyCollection,
    ssa_deps_collection: SSA_Collection,
    ssa_const_collection: ConstantCollection,
):
    """
    Build line-to-line dependencies.
    We iterate over all line dependencies in deps_collection, and find
    the corresponding SSA dependency in ssa_deps_collection. Then we can
    get the const value it depends on from ssa_const_collection, and finally
    get the line number of the const from deps_collection. At last, we can
    get a line-to-line dependency
    """
    dependencies = []
    for dep in deps_collection.values():
        dep: DependencyEntry
        ssa_dep: SSA_Dep = ssa_deps_collection.find_dependency(dep.block_id, dep.index)
        if ssa_dep is None:
            logger().debug(f"SSA dependency not found for: {dep.to_dict()}")
            continue
        for ident, id in ssa_dep.values():
            const_entry: ConstantEntry = ssa_const_collection.find(ident, id)
            if const_entry is None:
                logger().debug(f"SSA constant not found for: {ident} {id}")
                continue
            dependencies.append({"src": dep.to_dict(), "dst": const_entry.to_dict()})
    return dependencies


def extract_paths(dependencies):
    """
    Extract simple paths from dependencies, which means,
    only keep lineno information.
    """
    paths = []
    for dep in dependencies:
        path = (dep["src"]["lineno"], dep["dst"]["lineno"])
        if path not in paths:
            paths.append(path)
    return paths
