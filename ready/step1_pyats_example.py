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


class VerifyLogging(aetest.Testcase):
    """
    VerifyLogging Testcase - collect show logging information from devices
    Verify that all devices do not have 'ERROR|WARN' messages in logs
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and run error_logs testcase for each device
        :return:
        """

        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.error_logs, device=devices)

    @aetest.test
    def error_logs(self, device):
        """
        Verify that all devices do not have 'ERROR|WARN' messages in logs
        """

        output = device.execute('show logging | i ERROR|WARN')

        if len(output) > 0:
            self.failed('Found ERROR in log, review logs first')
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
