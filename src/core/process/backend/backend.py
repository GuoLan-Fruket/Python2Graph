import threading
import time
from core.db.client import DbClient
from core.process.collector import Collector
from core.process.process import ProcessDescriptor
from lib.shared.logger import logger
from lib.shared.task_util import Task

# Each worker should at least have 64 vertices or edges to process.
MINIMAL_TASK_COUNT = 64


class BackendDescriptor(ProcessDescriptor):
    def __init__(
        self,
        client: DbClient,
        source: Collector.Source,
        batch_size=500,
        max_workers=0,
        vertex_batch_size=None,
        edge_batch_size=None,
    ) -> None:
        super().__init__(max_workers)
        self.client: DbClient = client
        self.source: Collector.Source = source
        self.batch_size = max(1, batch_size)
        self.vertex_batch_size = (
            None if vertex_batch_size is None else max(1, vertex_batch_size)
        )
        self.edge_batch_size = (
            None if edge_batch_size is None else max(1, edge_batch_size)
        )

    def get_process(self) -> Task:
        return Task(self._process)

    def _process(self):
        # Add vertices first.
        workers = []
        worker_count = max(
            1, min(self.max_workers, self.source.vertex_count() // MINIMAL_TASK_COUNT)
        )
        clients = [
            self.client if i == 0 else self.client.clone() for i in range(worker_count)
        ]
        for i in range(worker_count):
            worker = threading.Thread(
                target=self._vertex_worker,
                args=(f"No.{i}", clients[i]),
            )
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

        # Optional sleep to let vertices be indexed.
        # time.sleep(1)

        # Add edges.
        workers = []
        worker_count = max(
            1, min(self.max_workers, self.source.edge_count() // MINIMAL_TASK_COUNT)
        )
        while worker_count > len(clients):
            clients.append(self.client.clone())
        for i in range(worker_count):
            worker = threading.Thread(
                target=self._edge_worker,
                args=(f"No.{i}", clients[i]),
            )
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

    def _vertex_worker(self, name, client: DbClient):
        logger().debug(f"Backend worker {name} started to add vertices...")

        # adding vertices
        batch_size = (
            self.batch_size
            if self.vertex_batch_size is None
            else self.vertex_batch_size
        )
        count = 0
        batch = []
        while True:
            vertex = self.source.get_vertex()
            if vertex is None:
                self.source.seal_vertex()
                break
            batch.append(vertex)
            count = count + 1
            if count == batch_size:
                logger().info(f"Adding {count} vertices.")
                client.add_vertex_bulk(batch)
                batch = []
                count = 0
        if count > 0:
            logger().info(f"Adding {count} vertices.")
            client.add_vertex_bulk(batch)
            batch = []
            count = 0

        logger().debug(f"Backend worker {name} finished adding vertices...")

    def _edge_worker(self, name, client: DbClient):
        logger().debug(f"Backend worker {name} started to add edges...")

        # adding edges
        batch_size = (
            self.batch_size if self.edge_batch_size is None else self.edge_batch_size
        )
        count = 0
        batch = []
        while True:
            edge = self.source.get_edge()
            if edge is None:
                self.source.seal_edge()
                break
            batch.append(edge)
            count = count + 1
            if count == batch_size:
                logger().info(f"Adding {count} edges.")
                client.add_edge_bulk(batch)
                batch = []
                count = 0
        if count > 0:
            logger().info(f"Adding {count} edges.")
            client.add_edge_bulk(batch)
            batch = []
            count = 0

        logger().debug(f"Backend worker {name} finished adding edges...")


def get_backend_descriptor(
    client: DbClient,
    source: Collector.Source,
    batch_size=500,
    max_workers=0,
    vertex_batch_size=None,
    edge_batch_size=None,
):
    return BackendDescriptor(
        client, source, batch_size, max_workers, vertex_batch_size, edge_batch_size
    )
