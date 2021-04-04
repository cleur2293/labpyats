#!/usr/bin/env python3.7

import logging
import os
import shlex
import shutil
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

        lab_guide_name = 'Lab_Guide.docx'
        lab_guide_path = os.path.join(dir, 'dr', lab_guide_name)
        lab_guide_move = os.path.join('/mnt/c/Users/Administrator/Desktop/', lab_guide_name)

        if os.path.exists(lab_guide_path):
            logger.info(f'Lab guide found')
            shutil.move(lab_guide_path, lab_guide_move)
            logger.info(f'Lab guide moved')
        else:
            logger.error(f'Lab guide not found')

if __name__ ==  '__main__':
    if len(sys.argv) == 2:
        dir = sys.argv[1]
        logger.debug(f'dir: {dir}')
        main(dir)
    else:
        logger.error(f'Incorrect number of arguments passed. Expected 1 got: {len(sys.argv)-1}')
        exit(1)


