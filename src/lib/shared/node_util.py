import ast
import json
import astor


class SrcNode:
    def __init__(self, node, code, line_no, char_no):
        self.node = node
        self.code = code
        self.line_no = line_no
        self.char_no = char_no


def to_src_without_children(node) -> SrcNode:
    if isinstance(node, ast.FunctionDef):
        node = ast.copy_location(
            ast.FunctionDef(
                name=node.name,
                args=node.args,
                body=[],
                decorator_list=node.decorator_list,
            ),
            node,
        )
    elif isinstance(node, ast.ClassDef):
        node = ast.copy_location(
            ast.ClassDef(
                name=node.name,
                bases=node.bases,
                keywords=node.keywords,
                body=[],
                decorator_list=node.decorator_list,
            ),
            node,
        )
    elif isinstance(node, ast.If):
        node = ast.copy_location(ast.If(test=node.test, body=[], orelse=[]), node)
    elif isinstance(node, ast.While):
        node = ast.copy_location(ast.While(test=node.test, body=[], orelse=[]), node)
    elif isinstance(node, ast.For):
        node = ast.copy_location(
            ast.For(target=node.target, iter=node.iter, body=[], orelse=[]), node
        )
    elif isinstance(node, ast.Try):
        node = ast.copy_location(
            ast.Try(body=[], handlers=[], orelse=[], finalbody=[]), node
        )
    elif isinstance(node, ast.With):
        node = ast.copy_location(ast.With(items=node.items, body=[]), node)

    # Append the line number to the source code
    code = astor.to_source(node).strip().replace("\n", "")
    lineno = get_node_lineno(node)
    col_offset = get_node_col_offset(node)

    if lineno is None or col_offset is None:
        raise Exception("Cannot find line number or col_offset for node")

    return SrcNode(node, code, lineno, col_offset)


def get_node_lineno(node):
    if hasattr(node, "lineno"):
        return node.lineno
    if node != None:
        for child in ast.iter_child_nodes(node):
            line_no = get_node_lineno(child)
            if line_no is not None:
                return line_no
    return None


def get_node_col_offset(node):
    if hasattr(node, "col_offset"):
        return node.col_offset
    if node != None:
        for child in ast.iter_child_nodes(node):
            col_offset = get_node_col_offset(child)
            if col_offset is not None:
                return col_offset

    return None


def get_node_line_no(node) -> int:
    if hasattr(node, "lineno"):
        return node.lineno
    if node != None:
        for child in ast.iter_child_nodes(node):
            line_no = get_node_line_no(child)
            if line_no is not None:
                return line_no

    raise Exception("Cannot find line number for node")
