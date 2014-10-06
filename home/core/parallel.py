"""This module contains utilities for parallelism within the Singleton
home.Core instance
"""
from multiprocessing import cpu_count


class ProcessPool:
    """A Lightweght Pool object responsible for spinning up and running multiple
    Python processes for running instances of executable in parallel
    """
    def __init__(self, executable=None, process_count=None, args=None):
        """Create a ProcessPool instance

        :param executable: A function or method to be run across multiple Python
            instances
        :param process_count: The maximum number of processes to be run in
            parallel. Defaults to cpu_count() * 2
        :param args: list of args and kwargs to pass to executable at run time
        """
        self._callable = executable
        self.process_count = process_count or cpu_count() * 2
        self.args = args or []

    def run(self):
        if self._callable is not None:
            pass

    def add_task_args(self, args):
        self.args.append(args)

    def map(self):
        pass

    @property
    def callable(self):
        return self._callable
    @callable.setter
    def callable(self, value):
        if hasattr(value, '__call__'):
            self._callable = value
