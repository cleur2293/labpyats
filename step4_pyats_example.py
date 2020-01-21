#!/bin/env python

# To get a logger for the script
import logging
import re

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handel errors with connections to devices
from unicon.core import errors

# Get your logger for your script
log = logging.getLogger(__name__)
log.level = logging.INFO

class MyCommonSetup(aetest.CommonSetup):

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


class PingTestcase(aetest.Testcase):

    @aetest.setup
    def setup(self):

        # list to store all IPs from topology
        dest_ips = []

        nx = self.parent.parameters['testbed'].devices['nx-osv-1']
        csr = self.parent.parameters['testbed'].devices['csr1000v-1']

        # Find links between Nx-os device and CSR100v
        dest_links = nx.find_links(csr)

        for links in dest_links:
            # process each link between devices

            for iface in links.interfaces:
                # process each interface (side) of the linki
                if iface.ipv4 is not None:
                    log.info(f'{iface.name}:{iface.ipv4.ip}')
                    dest_ips.append(iface.ipv4.ip)
                else:
                    log.info(f'Skipping iface {iface.name} without IPv4 address')

        log.info(f'Collected following IP addresses: {dest_ips}')

        # execute loop for ping test

        aetest.loop.mark(self.ping, dest_ip=dest_ips)

    @aetest.test
    def ping(self, dest_ip):
        """
       Sending 5, 56-bytes ICMP Echos to 10.0.0.18
       Timeout is 2 seconds, data pattern is 0xABCD

       64 bytes from 10.0.0.18: icmp_seq=0 ttl=255 time=0.594 ms
       64 bytes from 10.0.0.18: icmp_seq=1 ttl=255 time=0.837 ms
       64 bytes from 10.0.0.18: icmp_seq=2 ttl=255 time=0.761 ms
       64 bytes from 10.0.0.18: icmp_seq=3 ttl=255 time=0.594 ms
       64 bytes from 10.0.0.18: icmp_seq=4 ttl=255 time=0.565 ms

       --- 10.0.0.18 ping statistics ---
       5 packets transmitted, 5 packets received, 0.00% packet loss
       round-trip min/avg/max = 0.565/0.67/0.837 ms

       """

        nx = self.parent.parameters['testbed'].devices['nx-osv-1']

        try:
            result = nx.ping(dest_ip)
        except Exception as e:
            self.failed(f'Ping from {nx.name}->{dest_ip} failed: {e}')
        else:
            m = re.search(r"(?P<rate>\d+)\.\d+% packet loss", result)
            loss_rate = m.group('rate')

            if int(loss_rate) < 20:
                self.passed(f'Ping loss rate {loss_rate}%')
            else:
                self.failed('Ping loss rate {loss_rate}%')


if __name__ == '__main__':  # pragma: no cover

    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
