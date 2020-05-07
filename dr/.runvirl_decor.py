#!/usr/bin/env python3

from typing import Tuple
from time import sleep

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


def run_command(command, iter_count):
    def decorator_func(func):
        def wrap_func():
            logger.debug(f'running command: {command}')

            command_run = shlex.split(command)
            labpyats_dir = os.path.expanduser('~/labpyats')

            result = subprocess.run(command_run, stdout=subprocess.PIPE, cwd=labpyats_dir)
            output = result.stdout.decode('utf-8')
            output_lines = output.splitlines()

            result = None

            if (len(output_lines) > iter_count) and (not result):
                for line in output_lines:
                    print(f'output_line = {line}')
                    line_words_list = line.split()
                    result = func(line_words_list)

                    if result:
                        break

            print(f'****************************')
            return result

        return wrap_func

    return decorator_func


@run_command('virl ls', iter_count=5)
def check_topology_running(line_words_list) -> Tuple:
    if (len(line_words_list)>1):
        topology_name = line_words_list[1]
        if topology_name.startswith('labpyats'):
            if line_words_list[3]:
                topology_state = line_words_list[3]
                return True, topology_name, topology_state
            else:
                return False, topology_name, 'Unable to fetch current topology state'


@run_command('virl nodes', iter_count=3)
def check_virl_nodes(line_words_list):
    if (len(line_words_list)>5):
        node_state = line_words_list[5]
        if node_state.lower() == 'shutoff':
            print('need to shutoff')
            return True
        else:
            return False


def main() -> None:
	topology_result = check_topology_running()

	if topology_result:
		if topology_result[0]:
			virl_node_state = check_virl_nodes()
			if virl_node_state:
				print('send command to shutdown virl')
				sleep(2)
				print('send command to up virl')
			else:
				print(f'Nothing to do because topology "{topology_result[1]}" is in "{topology_result[2]}" state')
		else:
			print(f'ERROR: Unable to fetch current state of "{topology_result[1]}"')


if __name__ ==  '__main__':
    init_logging()
    main()


