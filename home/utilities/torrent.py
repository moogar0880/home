import os
import logging
from transmissionrpc.client import Client
from subprocess import call

from .core import SubprocessBase


class Transmission(Client, SubprocessBase):
    _name = 'Transmission'

    def __init__(self, path='/Applications', *args, **kwargs):
        """Create an instance of a Transmission client. If Transmission is not
        currently running, then it will be started. If it is running, the PID is
        grabbed in case Transmission needs to be killed.
        """
        super(Transmission, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger('Transmission')
        transmission = 'Transmission.app/Contents/MacOS/Transmission'
        self.executable = os.sep.join([path, transmission])
        self.pid = None
        if not self.running:
            output = call(self.executable, shell=True)
            self._logger.debug(output)
            if not self.running:
                self._logger.warn('Unable to start Transmission')
        self.client = Client()

    def stop_all(self):
        """Stop all currently running torrents"""
        self.client.stop_torrent([tor.id for tor in self.client.get_torrents()])

if __name__ == '__main__':
    transmission = Transmission()
    print(transmission.running)
    print(transmission.pid)
    from datetime import datetime
    start = datetime.now()
    transmission.stop_all()
    # transmission.kill()
    # It takes roughly 0:00:00.189425 to stop_all AND kill
    print(datetime.now() - start)
