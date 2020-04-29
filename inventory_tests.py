#!/bin/env python

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handel errors with connections to devices
from unicon.core import errors

# Get your logger for your script
log = logging.getLogger(__name__)

contract_sn = ['9L4HMKRV8NX', '9AH4C9TU2WP', '9JBG172PCVG']


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for testcases
    Establishes connections to all devices in testbed
    """

    @aetest.subsection
    def establish_connections(self, testbed):
        """
        Establishes connections to all devices in testbed
        :param testbed:
        :return:
        """

        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
            except errors.ConnectionError:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class InventoryTests(aetest.Testcase):
    """
    Inventory Testcase - extract Serial numbers information from devices
    Verify that all SNs are covered by service contract (exist in contract_sn)
    """
    
    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and run inventory testcase for each device
        :return:
        """
        
        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.inventory, device=devices)

    @aetest.test
    def inventory(self, device):
        """
        Verify that all SNs are covered by service contract (exist in contract_sn)
        :return:
        """
        
        if device.os == 'iosxe':

            out1 = device.parse('show inventory')
            chassis_sn = out1['main']['chassis']['CSR1000V']['sn']

            if chassis_sn not in contract_sn:
                self.failed(f'SN: {chassis_sn} is not covered by contract.')
            else:
                log.info(f'SN: {chassis_sn} is covered by the service contract.')

        elif device.os == 'nxos':

            out3 = device.parse('show inventory')
            chassis_sn = out3['name']['Chassis']['serial_number']

            if chassis_sn not in contract_sn:
                self.failed(f'SN: {chassis_sn} is not covered by contract.')
            else:
                log.info(f'SN: {chassis_sn} is covered by the service contract.')

        elif device.os == 'asa':

            out2 = device.parse('show inventory')
            chassis_sn = out2['Chassis']['sn']

            if chassis_sn not in contract_sn:
                self.failed(f'SN: {chassis_sn} is not covered by contract.')
            else:
                log.info(f'SN: {chassis_sn} is covered by the service contract.')


if __name__ == '__main__':  # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
