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


class Logging(aetest.Testcase):

    @aetest.setup
    def setup(self):
        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.logging, device=devices)

    @aetest.test
    def logging(self,device):

       output = device.execute('show logging | i ERROR|WARN')

       if len(output) > 0:
         """
         show logging | i ERROR|WARN
         asav-1#
         """         

         self.failed('Found ERROR in log, review them first')
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

