# -*- coding: utf-8 -*-
from subprocess import call, check_output, CalledProcessError

__author__ = 'Jon Nappi'


class SubprocessBase:
    """Python base class for Subprocesses, providing some common hooks into the
    subprocess itself
    """
    _path = _logger = _name = _pid = None

    @property
    def running(self):
        """Whether or not the client is currently running."""
        return self._is_running()

    def _is_running(self):
        """Check to see if there is already an instance of this process running
        """
        grep_cmd = 'ps aux | grep {}'.format(self._name)
        out = check_output(grep_cmd, shell=True).decode()
        for line in out.split('\n'):
            if self._path in line:
                data = line.split()
                self._pid = data[1]
                return True
        return False

    def kill(self, nine=False):
        """Kill the current process. If *nine* is ``True`` then the Process will
        be kill -9'd. Otherwise it will just be killed
        """
        if nine:
            command = 'kill -9 {}'.format(self._pid)
        else:
            command = 'kill {}'.format(self._pid)
        call(command, shell=True)

    def _execute(self, command):
        """Execute a command. Method should be overwritten by subclasses to
        provide more specific implementation of command execution
        """
        if self._path not in command:
            command = ' '.join([self._path, command])
        try:
            self._logger.debug(command)
            ret_val = check_output(command, shell=True)
        except CalledProcessError as e:
            ret_val = e.output
            self._logger.error(e.output)
        return ret_val
