#!/usr/bin/env python3

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
    log_formatter_file = logging.Formatter('%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s')

    console = logging.StreamHandler()
    console.setFormatter(log_formatter_console)
    console.setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler('/var/tmp/pyats_lab.log', maxBytes=(1048576 * 10), backupCount=10, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter_file)

    logger.addHandler(console)
    logger.addHandler(file_handler)


def run_command(command: str) -> str:
    logger.debug(f'running command: {command}')

    command_run = shlex.split(command)
    labpyats_dir = os.path.expanduser('~/labpyats')

    result = subprocess.run(command_run, stdout=subprocess.PIPE, cwd=labpyats_dir)
    output = result.stdout.decode('utf-8')
    return output


def main() -> None:
    output = run_command('virl ls')
    output_lines = output.splitlines()
    if len(output_lines) > 5:
        for line in output_lines:
            logger.debug(f'output_line = {line}')
            line_words_list = line.split()
            if (len(line_words_list) > 1):
                topology_name = line_words_list[1]
                if (topology_name.startswith('labpyats')):
                    if line_words_list[3]:
                        topology_state = line_words_list[3]
                        logger.info(f'Nothing to do because topology "{topology_name}" is in "{topology_state}" state')
                    else:
                        logger.error(f'ERROR: Unable to fetch current state of "{topology_name}"')

    elif len(output_lines) == 5:
        logger.info('No topology running, starting virl topology')
        output = run_command('virl up')
        logger.info(output)

    else:
        logger.error('ERROR: Unable to parse output of virl ls. Start topology with "virl up" manually')


if __name__ ==  '__main__':
    init_logging()
    main()


