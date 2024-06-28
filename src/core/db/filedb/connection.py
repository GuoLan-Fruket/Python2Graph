"""
Connection definition for FileDB.
"""

from core.db.filedb.filedb_client import FileDbClient


_VERTEX_FILE = None
_EDGE_FILE = None


def resolve_filedb(section: dict):
    """
    FILEDB:
      VERTEX_FILE: "./tmp/vertex.json"
      EDGE_FILE: "./tmp/edge.json"
    """
    global _VERTEX_FILE, _EDGE_FILE
    _VERTEX_FILE = section["VERTEX_FILE"]
    _EDGE_FILE = section["EDGE_FILE"]


def get_filedb_client() -> FileDbClient:
    if _VERTEX_FILE is None or _EDGE_FILE is None:
        raise Exception("FileDB connection is not initialized")
    return FileDbClient(_VERTEX_FILE, _EDGE_FILE)
