#!/usr/bin/env python3
"""The Core of the automation System"""
import logging
from multiprocessing import Process, cpu_count

# Core modules
from home.core.parallel import ProcessPool
from home.core.packages import site_packages

# Core Utility Modules
from home.utilities.vpn import Tunnelblick
from home.utilities.torrent import Transmission


class Core(object):
    """The Core of the system. Has interfaces for handling interactions with
    the rest of the system.
    """
    def __init__(self):
        super(Core, self).__init__()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('Core')
        pool_size = cpu_count() * 2
        self.pool = ProcessPool(process_count=pool_size)
        self.logger.debug('Cores: {}'.format(cpu_count()))
        self.processes = []
        self.vpn = Tunnelblick()
        self.transmission = Transmission()
        # Ensure that dependencies are always up to date when accessing the core
        site_packages(update=True)

    def __run_no_block(self, target, args=None, kwargs=None):
        """Span a new thread for running target with the provided args and
        kwargs and do not wait for it to complete. Any target passed to this
        needs to be trusted to actually complete since no join call is made.

        :param target: Any python object with a __call__ attribute
        :param args: args to be passed to the call to target
        :param kwargs: kwargs to be passed to the call to target
        """
        my_args = args or tuple()
        my_kwargs = kwargs or dict()
        Process(target=target, args=my_args, kwargs=my_kwargs).start()

    def __run(self, target, args=None, kwargs=None):
        """Span a new thread for running target with the provided args and
        kwargs and wait for it to complete.

        :param target: Any python element with a __call__ attribute
        :param args: args to be passed to the call to target
        :param kwargs: kwargs to be passed to the call to target
        """
        my_args = args or tuple()
        my_kwargs = kwargs or dict()
        proc = Process(target=target, args=my_args, kwargs=my_kwargs)
        proc.start()
        proc.join()

if __name__ == '__main__':
    core = Core()
    print(core)
    site_packages(install='requests')
    site_packages(update=True)
