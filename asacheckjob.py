import os
from ats.easypy import run

def main():
    # Find the location of the script in relation to the job file
    asa_health_tests = os.path.join('./step7_pyats_example.py')

    # Execute the testscript
    run(testscript=asa_health_tests)


