#!/bin/env python

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# Get your logger for your script
log = logging.getLogger(__name__)

contract_sn = ['923C9IN3KU1','93NA29NSARX','9AHA4AWEDBR']

class common_setup(aetest.CommonSetup):


    @aetest.subsection
    def establish_connections(self,testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class Inventory(aetest.Testcase):

    @aetest.setup
    def setup(self):
        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.inventory, device=devices)

    @aetest.test
    def inventory(self,device):

       if device.os == ('iosxe'):

         out1 = device.parse('show inventory')
         chassis_sn = out1['main']['chassis']['CSR1000V']['sn']

         if chassis_sn not in contract_sn:
             self.failed(f'{chassis_sn} is not covered by contract')
         else:
             pass

       elif device.os == 'nxos':

         out3 = device.parse('show inventory')
         chassis_sn = <<replace me>>

         if chassis_sn not in contract_sn:
             self.failed(f'{chassis_sn} is not covered by contract')
         else:
             pass

       elif device.os == 'asa':

         out2 = device.parse('show inventory')
         chassis_sn = <<replace me>>

         if chassis_sn not in contract_sn:
             self.failed(f'{chassis_sn} is not covered by contract')
         else:
             pass


if __name__ == '__main__': # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))

