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

golden_routes = ['192.168.0.3/32', '192.168.0.1/32']


class common_setup(aetest.CommonSetup):

    @aetest.subsection
    def establish_connections(self, testbed):
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

    @aetest.setup
    def setup(self):
        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.routes, device=devices)

    @aetest.test
    def routes(self, device):

        if device.os == ('iosxe' or 'nxos'):

            output = device.learn('routing')
            rib = output.info['vrf']['default']['address_family']['ipv4']['routes']

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
