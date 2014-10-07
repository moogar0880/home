# -*- coding: utf-8 -*-
import logging
from importlib import reload
from subprocess import check_output

INSTALLED_PACKAGES = ('requests', 'python-crontab', 'ThePirateBay',
                      'transmissionrpc')
EASY_INSTALL = []


def easy_install():
    """Run easy install on all packages in the EASY_INSTALL tuple"""
    logger = logging.getLogger('easy_install')
    for package in EASY_INSTALL:
        install_cmd = 'easy_install {}'.format(package)
        logger.info(install_cmd)
        response = check_output(install_cmd, shell=True).decode('UTF-8')
        dbg = ': '.join([install_cmd, response])
        logger.debug(dbg)


def site_packages(install=None, update=False):
    """A functional interface to site_packages package directory. By passing
    parameters to *install* (either a ``list`` or ``str``) a package will be
    installed via pip. If *update* is set to ``True``, all of the packages
    installed will be checked to see if they can be updated, if they can, then
    they're updated.
    """
    logger = logging.getLogger('site-packages')
    if install is not None:
        if isinstance(install, list):
            for package in install:
                install_cmd = 'pip install {}'.format(package)
                logger.info(install_cmd)
                response = check_output(install_cmd, shell=True).decode('UTF-8')
                dbg = 'pip install {}: {}'.format(package, response)
                logger.debug(dbg)
        elif isinstance(install, str):
            install_cmd = 'pip install {}'.format(install)
            logger.info(install_cmd)
            response = check_output(install_cmd, shell=True).decode('UTF-8')
            dbg = 'pip install {}: {}'.format(install, response)
            logger.debug(dbg)
    if update:
        freeze = 'pip freeze'
        before = check_output(freeze, shell=True).decode('UTF-8')
        pre_update = [tuple(entry.split('==')) for entry in before.split()]
        update_command = ' '.join(['pip', 'freeze', '--local', '|', 'grep',
                                   '-v', "'^\-e'", '|', 'cut', '-d', '=', '-f',
                                   '1', '|', 'xargs', 'pip', 'install', '-U'])
        results = check_output(update_command, shell=True).decode('UTF-8')
        dbg = 'pip upgrade: {}'.format(results)
        logger.debug(dbg)
        after = check_output(freeze, shell=True).decode('UTF-8')
        post_update = [tuple(entry.split('==')) for entry in after.split()]
        for pre, post in zip(pre_update, post_update):
            package = pre[0]
            v1 = pre[1]
            v2 = post[1]
            if v2 != v1:
                logger.info('Reloading {}'.format(package))
                reload(__import__(package))
