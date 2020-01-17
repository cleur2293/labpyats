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

      nx = self.parent.parameters['testbed'].devices['nx-osv-1']
      csr = self.parent.parameters['testbed'].devices['csr1000v-1']
      
      # Find links between Nx-os device and CSR100v
      dest_links = nx.find_links(csr)
      dest_ips = []

      for links in dest_links:
         # process each link between devices

         for iface in links.interfaces:
            # process each interface (side) of the linki
            if iface.ipv4 is not None:
              print(f'{iface.name}:{iface.ipv4.ip}')
              dest_ips.append(iface.ipv4.ip)
            else:
              print(f'Skipping iface {iface.name} without IPv4 address')
      
      print(f'Collected following IP addresses: {dest_ips}')
      
      # execute loop for ping test

      aetest.loop.mark(self.ping, dest_ips = dest_ips)

    @aetest.test
    def ping(self,dest_ips):

       result =  nx = self.parent.parameters['testbed'].devices['nx-osv-1'].ping(dest_ips)


if __name__ == '__main__': # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))

