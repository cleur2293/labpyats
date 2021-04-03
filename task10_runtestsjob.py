import os
from ats.easypy import run
from pyats.topology.loader import load

def main():
    # Find the location of the script in relation to the job file
    ping_tests = os.path.join('task9_labpyats.py')
    testbed = load('pyats_testbed.yaml')

    # Execute the testscript
    run(testscript = ping_tests, pyats_testbed = testbed)

