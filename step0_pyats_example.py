#!/usr/bin/env python3

import logging

from genie.conf import Genie

from os import path
from os import mkdir

# To handle errors with connections to devices
from unicon.core import errors


def create_non_existing_dir(dir_path):
    if not path.exists(dir_path):
        try:
            mkdir(dir_path)
        except PermissionError as e:
            log.error(f'Unable to create directory: {dir_path}. Insufficient privileges. Error: {e}')
            exit(1)


def write_commands_to_file(abs_filename, command_output):
    try:
        with open(abs_filename, "w") as file_output:
            file_output.write(command_output)

    except IOError as e:
        log.error(f'Unable to write output to file: {abs_filename}. Due to error: {e}')
        exit(1)


def collect_device_commands(testbed, commands_to_gather, dir_name):
    abs_dir_path = path.join(path.dirname(__file__), dir_name)

    create_non_existing_dir(abs_dir_path)

    for device_name, device in testbed.devices.items():

        device_os = device.os  # get operating system of a device from pyats_testbed.yaml
        device_path = path.join(abs_dir_path, device_name)
        create_non_existing_dir(device_path)

        try:
            device.connect()
        except errors.ConnectionError:
            log.error(f'Failed to establish connection to: {device.name}. Check connectivity and try again.')
            continue

        device.connectionmgr.log.setLevel(logging.ERROR)
        device.log_user(enable=True)

        if commands_to_gather.get(device_os):
            for command in commands_to_gather[device_os]:
                filename_command = command.replace(' ', '_')
                filename_command = filename_command.replace('*', 'all')
                filename = device_name + '_' + filename_command
                abs_filename = path.join(device_path, filename)
                log.info(f'filename = {abs_filename}')

                command_output = device.execute(command)

                write_commands_to_file(abs_filename, command_output)
        else:
            log.error(f'No commands for operating system: {device_os} of device: {device_name} has been defined. '
                      f'This device has been skipped. Specify list of commands for {device_os} and try again.')
            continue


def main():
    global log
    log = logging.getLogger(__name__)
    log.level = logging.INFO

    testbed_filename = '/home/cisco/labpyats/pyats_testbed.yaml'
    testbed = Genie.init(testbed_filename)

    commands_to_gather = {
        'asa': ['show inventory', 'show running-config', 'show route',
                'show ospf neighbor', 'show license all'],
        'iosxe': ['show inventory', 'show running-config', 'show ip route vrf *',
                  'show ip ospf neighbor', 'show license feature'],
        'nxos': ['show inventory', 'show running-config', 'show ip route vrf all',
                 'show ip ospf neighbor vrf all', 'show license usage']}

    dir_name = 'gathered_commands'

    collect_device_commands(testbed, commands_to_gather, dir_name)


if __name__ == '__main__':
    main()
