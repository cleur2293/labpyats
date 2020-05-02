#!/usr/bin/env python3.7

import logging
import os
import shlex
import subprocess
import sys

global logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)


def main(dir: str) -> None:
    devnull = open(os.devnull, 'w')

    command_run = shlex.split(f'git clone https://github.com/cleur2293/labpyats.git {dir}')

    logger.debug(f'running command: {command_run}')

    code = subprocess.call(command_run, stderr=devnull)

    if code:
        if code == 128:
            logger.error(f'Unable to create Git Repo in directory: {dir}. This directory already exists.')
        else:
            logger.error(f'Unable to coplete "git clone" some error has happened')
    else:
        logger.info(f'git clone has finished successfully. Repo has been created in {dir}')

if __name__ ==  '__main__':
    if len(sys.argv) == 2:
        dir = sys.argv[1]
        logger.debug(f'dir: {dir}')
        main(dir)
    else:
        logger.error(f'Incorrect number of arguments passed. Expected 1 got: {len(sys.argv)-1}')
        exit(1)


