import os
from ats.easypy import run

def main():
    # Find the location of the script in relation to the job file
    ping_tests = os.path.join('./step4_pyats_example.py')

    # Execute the testscript
    run(testscript=ping_tests)


