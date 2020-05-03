#!/bin/env python

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handel errors with connections to devices
from unicon.core import errors

from pprint import pprint

import argparse
from pyats.topology import loader

# Import custom class for PyATS learn ('show counters')
from asaops import HealthASA

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
        Establishes connections to ASAs
        :param testbed:
        :return:
        """

        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            if device.os == 'asa':
                log.info(banner("Connect to device '{d}'".format(d=device.name)))
                try:
                    device.connect()
                except errors.ConnectionError:
                    self.failed("Failed to establish connection to '{}'".format(device.name))
                device_list.append(device)
            else:
                pass
        # Pass list of ASA devices to testcases
        self.parent.parameters.update(dev=device_list)


class VerifyASAHealth(aetest.Testcase):
    """
    VerifyASAHealth - collect telemetry information from ASA devices
    Verify that all devices  behaving correctly
    """

    @aetest.test
    def learn_asa_counters_info(self):
        self.all_asa_info = {}

        for dev in self.parent.parameters['dev']:
            log.info(banner("Gathering ASA health information {}".format(
                dev.name)))

            asahealth = HealthASA(dev)
            asahealth.learn()
            self.all_asa_info[dev.name] = asahealth.info

        log.info(f'\n\nResult of ASA health check:\n{self.all_asa_info}\n\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))


