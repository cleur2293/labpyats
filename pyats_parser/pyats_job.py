#!/bin/env python

from pyats.easypy import run

test_files = [
    'step1_pyats_example.py',
    'step2_pyats_example.py',
    'step3_pyats_example.py',
    'step4_pyats_example.py'
]


def main():
    for test_file in test_files:
        run(test_file)
