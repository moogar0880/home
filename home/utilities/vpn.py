# -*- coding: utf-8 -*-
import logging

from .core import SubprocessBase


class Air(SubprocessBase):
    """A persistent, scriptable, interface to the default AirVPN CLI"""
    _path = '/Applications/AirVPN.app/Contents/MacOS/AirVPN -cli'
    _name = 'AirVPN'

    def __init__(self):
        """Create an object capable of performing all of the operations allowed
        by the AirVPN CLI
        """
        super(Air, self).__init__()
        self._logger = logging.getLogger(str(self.__class__))
        self._is_running()

    def usage(self):
        """Return the usage of the AirVPN CLI"""
        return self._execute('-help')

    def login(self, username, password):
        """Attempt to login using the provided username and password"""
        command = '-login {} -password {}'.format(username, password)
        return self._execute(command)

    def start(self, config_name, mgt_port, use_scripts=None, skip_scr_sec=None,
              cfg_loc_code=None, no_monitor=None, bit_mask=None,
              leasewatch_options=None, openvpn_version=None):
        """Load the net.tunnelblick.tun and/or net.tunnelblick.tap kexts and
        start OpenVPN with the specified configuration file and options. foo.tun
        kext will be unloaded before loading net.tunnelblick.tun, and foo.tap
        will be unloaded before loading net.tunnelblick.tap.
        """
        args = [use_scripts, skip_scr_sec, cfg_loc_code, no_monitor, bit_mask,
                leasewatch_options, openvpn_version]
        command_args = ['start', str(config_name), str(mgt_port)]
        command_args += [str(x) for x in args if x is not None]
        command = ' '.join(command_args)
        return self._execute(command)


if __name__ == '__main__':
    tb = Air()
    print(tb.start('AirVPN_Europe.tblk', 0, 1, 0, 1, 0, 305, '-ptADGNWradsgnw',
                   '2.2.1'))
