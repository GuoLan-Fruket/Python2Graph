from typing import List
from core.graph.graph import GraphEdge, GraphVertex


class DbClient:
    """
    Database client interface. Should allow multiple instances?
    """

    def __init__(self) -> None:
        pass

    def clone(self):
        """
        Clone the database client. Used to create multiple instances
        with one prototype.
        """
        raise NotImplementedError

    def drop(self):
        """
        Drop the database.
        """
        raise NotImplementedError

    def init(self):
        """
        Initialize the database.
        """
        raise NotImplementedError

    def add_vertex(self, vertex: GraphVertex):
        """
        Add a vertex to the database.
        """
        raise NotImplementedError

    def add_vertex_bulk(self, vertices: List[GraphVertex]):
        """
        Add a list of vertices to the database.
        """
        raise NotImplementedError

    def add_edge(self, edge: GraphEdge):
        """
        Add an edge to the database.
        """
        raise NotImplementedError

    def add_edge_bulk(self, edges: List[GraphEdge]):
        """
        Add a list of edges to the database.
        """
        raise NotImplementedError
