import os
from ats.easypy import run

def main():
    # Find the location of the script in relation to the job file
    inventory_tests = os.path.join('inventory_tests.py')

    # Execute the testscript
    run(testscript=inventory_tests)


