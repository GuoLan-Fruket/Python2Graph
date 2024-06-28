"""
FileDB is a file-based database. It is used to store the graph data in a file.
The main purpose of this class is to provide a way to validate the graph data
when debugging on small graph on local machine. It should not be used in production.
"""

import threading
from typing import List
from core.graph.graph import GraphEdge, GraphVertex
from lib.shared.path_util import create_file, remove_file
from core.db.client import DbClient


class FileDbClient(DbClient):
    """
    FileDB client. Will output vertices and edges to two JSON files.
    The format of the file is one compact JSON object per line.
    """

    def __init__(self, vertex_file, edge_file) -> None:
        super().__init__()
        if vertex_file == edge_file:
            raise ValueError("Vertex file and edge file must be different.")
        self.vertex_file = vertex_file
        self.edge_file = edge_file

    def clone(self):
        return FileDbClient(self.vertex_file, self.edge_file)

    def drop(self):
        """
        This may not be thread safe.
        """
        remove_file(self.vertex_file)
        remove_file(self.edge_file)

    def init(self):
        self.drop()  # is this needed?
        create_file(self.vertex_file)
        create_file(self.edge_file)

    def add_vertex(self, vertex: GraphVertex):
        lock = threading.Lock()
        lock.acquire()
        with open(self.vertex_file, "a") as f:
            f.write(vertex.to_string(0))
            f.write("\n")
        lock.release()

    def add_vertex_bulk(self, vertices: List[GraphVertex]):
        lock = threading.Lock()
        lock.acquire()
        with open(self.vertex_file, "a") as f:
            for vertex in vertices:
                f.write(vertex.to_string(0))
                f.write("\n")
        lock.release()

    def add_edge(self, edge: GraphEdge):
        lock = threading.Lock()
        lock.acquire()
        with open(self.edge_file, "a") as f:
            f.write(edge.to_string(0))
            f.write("\n")
        lock.release()

    def add_edge_bulk(self, edges: List[GraphEdge]):
        lock = threading.Lock()
        lock.acquire()
        with open(self.edge_file, "a") as f:
            for edge in edges:
                f.write(edge.to_string(0))
                f.write("\n")
        lock.release()
