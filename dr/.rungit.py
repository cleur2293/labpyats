#!/usr/bin/env python3.7

import logging
import logging.handlers
import os
import shlex
import subprocess
import sys


def init_logging() -> None:
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_formatter_console = logging.Formatter('%(filename)s: %(message)s')
    format = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s'
    log_formatter_file = logging.Formatter(format)

    console = logging.StreamHandler()
    console.setFormatter(log_formatter_console)
    console.setLevel(logging.INFO)

    file_handler = \
        logging.handlers.RotatingFileHandler('/var/tmp/pyats_lab.log',
                                             maxBytes=(1048576 * 10),
                                             backupCount=10,
                                             encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter_file)

    logger.addHandler(console)
    logger.addHandler(file_handler)


def main(dir: str) -> None:
    devnull = open(os.devnull, 'w')

    command_run = \
        shlex.split(f'git clone '
                    f'https://github.com/cleur2293/labpyats.git {dir}')

    logger.debug(f'running command: {command_run}')

    code = subprocess.call(command_run, stderr=devnull)

    if code:
        if code == 128:
            logger.error(f'Unable to create Git Repo in directory: '
                         f'{dir}. This directory already exists.')
        else:
            logger.error(f'Unable to coplete "git clone". '
                         f'Unexpected error has happened')
    else:
        logger.info(f'git clone has finished successfully. '
                    f'Repo has been created in {dir}')


if __name__ == '__main__':
    init_logging()
    if len(sys.argv) == 2:
        dir = sys.argv[1]
        logger.debug(f'dir: {dir}')
        main(dir)
    else:
        logger.error(f'Incorrect number of arguments passed. '
                     f'Expected 1 got: {len(sys.argv)-1}')
        exit(1)
