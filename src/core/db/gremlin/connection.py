"""
This module is responsible for creating and managing the connection to the 
Gremlin server.
"""

from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.serializer import GraphSONMessageSerializer
from gremlin_python.structure.graph import Graph, GraphTraversalSource
from core.cache.cache_proxy import CacheProxy

from core.db.gremlin.gremlin_client import GremlinClient

# Gremlin connection is a singleton?
_GREMLIN_TRAVERSAL_SOURCE: GraphTraversalSource = None


def resolve_gremlin(section: dict):
    """
    GREMLIN:
      CONNECTION_STRING: "ws://ip:8182/gremlin"
    """
    _connect_gremlin(section["CONNECTION_STRING"])


class DummyGraphSONSerializer(GraphSONMessageSerializer):
    def __init__(self):
        super(DummyGraphSONSerializer, self).__init__(None, None, None)

    def build_message(self, request_id, processor, op, args):
        return "".encode("utf-8")


def _connect_gremlin(
    connection_string: str, traversal_source="g"
) -> GraphTraversalSource:
    """
    This function is not thread safe. It should be called only once.
    """
    global _GREMLIN_TRAVERSAL_SOURCE
    if _GREMLIN_TRAVERSAL_SOURCE is None:
        _GREMLIN_TRAVERSAL_SOURCE = (
            Graph()
            .traversal()
            .withRemote(DriverRemoteConnection(connection_string, traversal_source))
        )
    else:
        raise Exception("Gremlin connection is already initialized")
    return _GREMLIN_TRAVERSAL_SOURCE


def get_gremlin_client(cache: CacheProxy) -> GremlinClient:
    """
    Get a Gremlin client based on current configuration.
    This function should be called after resolve_gremlin.
    """
    if _GREMLIN_TRAVERSAL_SOURCE is None:
        raise Exception("Gremlin connection is not initialized")
    return GremlinClient(_GREMLIN_TRAVERSAL_SOURCE, cache)
