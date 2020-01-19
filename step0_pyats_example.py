import logging

from genie.conf import Genie

from os import path
from os import mkdir

from unicon.core import errors

log = logging.getLogger(__name__)
log.level = logging.INFO

testbed = './default_testbed.yaml'
testbed = Genie.init(testbed)


def create_non_existing_dir(dir_path):
    if not path.exists(dir_path):
        try:
            mkdir(dir_path)
        except PermissionError as e:
            log.error(f'Unable to create directory: {dir_path}. Insufficient privileges. Error: {e}')


def write_commands_to_file(abs_filename, command_output):
    try:
        with open(abs_filename, "w") as file_output:
            file_output.write(command_output)

    except IOError as e:
        log.error(f'Unable to write output to file: {abs_filename}. Due to error: {e}')

    except PermissionError as e:
        log.error(f'Unable to write output to file: {abs_filename}. Insufficient privileges. Error: {e}')

def main():
    commands_to_gather = {
    'asav-1': ['show inventory','show running-config', 'show route', 'show ospf neighbor', 'show license all'],
    'csr1000v-1': ['show inventory','show running-config', 'show ip route vrf *', 'show ip ospf neighbor', 'show license feature'],
    'nx-osv-1': ['show inventory','show running-config', 'show ip route vrf all', 'show ip ospf neighbor vrf all', 'show license usage']}

    dir_name = 'gathered_commands'
    abs_dir_path = path.join(path.dirname(__file__), dir_name)

    create_non_existing_dir(abs_dir_path)

    for device_name in testbed.devices:

        device_path =  path.join(abs_dir_path, device_name)
        create_non_existing_dir(device_path)

        device = testbed.devices[device_name]

        try:
            device.connect(stdout=False)
        except errors.ConnectionError:
            log.error(f'Failed to establish connection to: {device.name}. Check connectivity and try again.')
            continue

        device.connectionmgr.log.setLevel(logging.ERROR)
        # device.log_user(enable=False)

        for command in commands_to_gather[device_name]:
            filename = device_name + '_' + command
            abs_filename = path.join(device_path, filename)
            log.info(f'filename = {abs_filename}')

            command_output = device.execute(command)

            write_commands_to_file(abs_filename, command_output)

if __name__ == '__main__':
    main()


