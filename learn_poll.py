import logging



from genie import testbed
from genie.libs.ops.interface.nxos.interface import Interface

# Load Genie testbed
testbed = testbed.load(testbed='pyats_testbed.yaml')

nxos = testbed.devices['nx-osv-1']

nxos.connect()
nxos.connectionmgr.log.setLevel(logging.ERROR)

def verify_interface_status(obj):
            if obj.info['Ethernet1/4'].get('oper_status', None) and\
               obj.info['Ethernet1/4']['oper_status'] == 'up':
               print('+Eth1/4 is UP!!!!')
               return

            print('-Eth1/4 is still down!!!')
            raise Exception('Eth1/4 is down')

#nx_int =  nxos.learn('interface', attributes=['info[(.*)][oper_status]'])
nx_int =  nxos.learn('interface', attributes=['info["Ethernet1/4"][oper_status]'])

result = nx_int.learn_poll(verify=verify_interface_status, sleep=1, attempt=100)
