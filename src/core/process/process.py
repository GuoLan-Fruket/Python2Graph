"""
The whole generation includes two main processes: 
    Frontend graph generation and backend database generation.
These two processes can be described by a descriptor.
"""

from lib.shared.task_util import get_cpu_count


class ProcessDescriptor:
    """
    Descriptor for a process. Through this descriptor, we can get
    a process to run.
    """

    def __init__(self, max_workers=0) -> None:
        self.max_workers = self._auto_configure_max_worker(max_workers)

    def get_process(self):
        """
        Return the process function, a Task to invoke.
        """
        raise NotImplementedError

    def _auto_configure_max_worker(self, max_workers):
        return (
            get_cpu_count() if max_workers is None or max_workers <= 0 else max_workers
        )
