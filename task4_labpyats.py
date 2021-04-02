#!/usr/bin/env python3
import logging

from pyats.topology.loader import load

from os import path
from os import mkdir

# To handle errors with connections to devices
from unicon.core import errors


def write_commands_to_file(abs_filename, command_output):
    try:
        with open(abs_filename, "a+") as file_output:
            file_output.write(command_output)

    except IOError as e:
        log.error(f'Unable to write output to file: {abs_filename}.'
                  f'Due to error: {e}')
        exit(1)


def collect_device_commands(testbed, command_to_gather, filename):
    abs_filename = path.join(path.dirname(__file__), filename)
    log.info(f'filename: {abs_filename}')

    log.info('Starting to collect output of the commands')

    for device_name, device in testbed.devices.items():

        try:
            device.connect(log_stdout=False)
        except errors.ConnectionError:
            log.error(f'Failed to establish connection to: {device.name}.'
                      f'Check connectivity and try again.')
            continue

        else:
            log.info(f'Connected ok: {device_name}')
            command_output = device.execute(command_to_gather, log_stdout=True)
            write_commands_to_file(abs_filename, command_output + '\n####\n')


def main():
    global log
    format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=format)

    log = logging.getLogger(__name__)

    testbed_filename = '/home/cisco/labpyats/pyats_testbed.yaml'
    testbed = load(testbed_filename)

    output_filename = 'collected_task4'
    open(output_filename, 'w').close()

    dir_name = 'gathered_commands'

    collect_device_commands(testbed, 'show inventory' , output_filename)


if __name__ == '__main__':
    main()
