from genie.conf import Genie
from genie import parsergen

from pprint import pprint

import logging

testbed = Genie.init('pyats_testbed.yaml')

asa = testbed.devices['asav-1']

asa.connect()
asa.connectionmgr.log.setLevel(logging.ERROR)

show_counters = asa.device.execute('show counters')

print(f'command output: \n{show_counters}')

header = ['Protocol', 'Counter', 'Value', 'Context']

result = parsergen.oper_fill_tabular(device_output=show_counters, device_os='asa', header_fields=header, index=[1])

print('result:')
pprint(result.entries)

result_entries = result.entries

for counter_name in result_entries.keys():
    print(f'{counter_name} = {result_entries[counter_name]["Value"]}')


