from collections import deque
from core.db.client import DbClient
from core.db.gremlin.gremlin_client import GremlinClient
from lib.conf import CommitDiff
from lib.shared.logger import logger
from gremlin_python.structure.graph import GraphTraversalSource
from gremlin_python.process.graph_traversal import __


def _get_related_files(g: GraphTraversalSource, file: str) -> list:
    """
    Get all related files of the given file.
    """
    related = []
    related.extend(
        g.V().hasLabel("file").has("file", file).out("related").values("file").toList()
    )
    related.extend(
        g.V().hasLabel("file").has("file", file).in_("related").values("file").toList()
    )
    return related


def _get_affected_files(g: GraphTraversalSource, diff: CommitDiff) -> list:
    """
    Get all affected files by the given diff.
    """
    files_to_remove = []
    files_to_add = []
    for file, status in diff.enumerate():
        if status == "A":
            files_to_remove.append(file)
            files_to_add.append(file)
        else:
            files_to_remove.append(file)
            if status == "M":
                files_to_add.append(file)
            for related in _get_related_files(g, file):
                files_to_remove.append(related)
                if related not in diff.removed:
                    files_to_add.append(related)

    # remove duplication
    files_to_remove = list(set(files_to_remove))
    files_to_add = list(set(files_to_add))

    return files_to_remove, files_to_add


def _apply_diff_impl(client: GremlinClient, diff: CommitDiff) -> list:
    g = client.g()
    files_to_remove, files_to_add = _get_affected_files(client.g(), diff)

    # remove files
    for file in files_to_remove:
        g.V().has("file", file).drop().iterate()

    return files_to_add


def apply_diff(client: DbClient, diff: CommitDiff) -> list:
    """
    Apply the given diff to the database. And return all affected files.
    """
    if isinstance(client, GremlinClient):
        return _apply_diff_impl(client, diff)
    else:
        logger().warning("Diff is not supported for the given backend.")
        return None
