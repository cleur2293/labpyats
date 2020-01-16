#!/bin/env python

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# Get your logger for your script
log = logging.getLogger(__name__)

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


class PingTestcase(aetest.Testcase):

    @aetest.setup
    def setup(self):


      dest_ips = [] # list to store all IPs from topology

      for device in self.parent.parameters['dev']:
        for intf in device:
          print(f'{device.name}:{intf.name}:{intf.ipv4}')      

          
          dest_ips.append(str(intf.ipv4))

          result = self.parent.parameters['testbed'].devices['nx-osv-1'].ping('8.8.8.8')
          print(result)


    @aetest.test
    def ping(self):


      nx = self.parent.parameters['testbed'].devices['nx-osv-1']
      csr = self.parent.parameters['testbed'].devices['csr1000v-1']

      dest_links = csr.find_links(nx)
      
      for intf in csr.interfaces:
 #stopped here
        if intf.name in 
          dest_ip.append(str(intf.ipv4.ip))
        



      try:
            # store command result for later usage
            result =  self.parent.parameters['testbed'].devices['nx-osv-1'].ping(destination)






if __name__ == '__main__': # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))

