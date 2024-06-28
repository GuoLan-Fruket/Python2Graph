import os
import queue
import threading

from lib.shared.logger import logger


def get_cpu_count():
    return os.cpu_count() or 1


class Task:
    """
    A task is a tuple of (target, args).
    """

    def __init__(self, target, args=None):
        self.target = target
        self.args = args

    def invoke(self, **kwargs):
        """
        Invoke the task synchronously in the current thread.
        """
        if self.args is None:
            return self.target(**kwargs)
        return self.target(*self.args, **kwargs)

    def invoke_async(self, **kwargs):
        """
        Invoke the task asynchronously in a new thread, and return the thread object.
        This way, the return value of the task is not available directly.
        """
        task: threading.Thread = None
        if self.args is None:
            task = threading.Thread(target=self.target, kwargs=kwargs)
        else:
            task = threading.Thread(target=self.target, args=self.args, kwargs=kwargs)
        task.start()
        return task
