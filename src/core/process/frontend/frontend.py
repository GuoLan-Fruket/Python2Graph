"""
The process of frontend is described as follows:

1. A SINGLE producer that emits all files.
2. Multiple consumers to process the files.
3. All consumers then output the results to the sink.
"""

import queue
import threading
from lib.shared.logger import logger
from core.process.collector import Collector
from core.process.process import ProcessDescriptor
from lib.shared.task_util import Task


class FrontEndDescriptor(ProcessDescriptor):
    def __init__(
        self,
        root: str,
        producer: Task,
        consumer: Task,
        sink: Collector.Sink,
        max_workers=0,
    ) -> None:
        """
        :param root: the root folder to start with
        :param producer: if invoked, should emit all files as an enumeration
        :param consumer: if invoked with extra parameter (root, file, sink), should
            process the file, and output the results to the sink
        """
        super().__init__(max_workers)
        self.root: str = root
        self.producer: Task = producer
        self.consumer: Task = consumer
        self.sink: Collector.Sink = sink
        self.files = queue.Queue()

    def get_process(self) -> Task:
        return Task(self._process)

    def _process(self):
        workers = []
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker, args=(f"No.{i}",))
            workers.append(worker)

        producer = threading.Thread(target=self._producer)
        producer.start()
        for worker in workers:
            worker.start()
        producer.join()
        for worker in workers:
            worker.join()

    def _producer(self):
        logger().debug("Frontend producer started.")
        for file in self.producer.invoke():
            self.files.put(file)
        self.files.put(None)
        logger().debug("Frontend producer stopped.")

    def _worker(self, name):
        logger().debug(f"Frontend worker {name} started.")
        while True:
            file = self.files.get()
            if file is None:
                self.files.put(None)
                break
            self.consumer.invoke(root=self.root, file=file, sink=self.sink)
        logger().debug(f"Frontend worker {name} stopped.")
