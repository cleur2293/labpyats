#!/bin/env python

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handle erorrs in connections
from unicon.core import errors

# Get your logger for your script
log = logging.getLogger(__name__)

golden_routes = ['192.168.0.3/32', '192.168.0.1/32']


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


class Routing(aetest.Testcase):
    """
    Routing Testcase - extract routing information from devices
    Verify that all device have golden_routes installed in RIB
    """
    
    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and run routes testcase for each device
        :return:
        """
        
        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.routes, device=devices)

    @aetest.test
    def routes(self, device):
        """
        Verify that all device have golden_routes installed in RIB
        """
        
        if (device.os == 'iosxe') or (device.os == 'nxos'):

            output = device.learn('routing')
            rib = << replace me >>

            for route in golden_routes:
                if route not in rib:
                    self.failed(f'{route} is not found')
                else:
                    pass

        elif device.os == 'asa':
            output = device.parse('show route')
            rib = output['vrf']['default']['address_family']['ipv4']['routes']

            for route in golden_routes:
                if route not in rib:
                    self.failed(f'{route} is not found')
                else:
                    pass


if __name__ == '__main__':  # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
