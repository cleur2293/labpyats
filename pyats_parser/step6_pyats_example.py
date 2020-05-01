from genie.conf import Genie
from genie import parsergen

from pprint import pprint


testbed = Genie.init('pyats_testbed.yaml')
asa = testbed.devices['asav-1']
asa.connect()

show_cmds = {
     'asa': {
        'show_cpu_sorted' : "show processes cpu-usage sorted non-zero",
     }
}

regex = {

    'asa': {
        'cpu.pc': r'\s*([0-9a-fx-]+)\s+[0-9_a-fx-]+\s+[0-9\.]+%\s+[0-9\.]+%\s+[0-9\.]+%\s+[a-zA-Z0-9_\s-]+',
        'cpu.thread': r'\s*[x0-9a-f-]+\s+([x0-9a-f-]+)\s+[0-9\.]+%\s+[0-9\.]+%\s+[0-9\.]+%\s+[a-zA-Z0-9_\s-]+',
        'cpu.5sec': r'\s*[x0-9a-f-]+\s+[x0-9a-f-]+\s+([0-9\.]+%)\s+[0-9\.]+%\s+[0-9\.]+%\s+[a-zA-Z0-9_\s-]+',
        'cpu.1min': r'\s*[x0-9a-f-]+\s+[x0-9a-f-]+\s+[0-9\.]+%\s+([0-9\.]+%)\s+[0-9\.]+%\s+[a-zA-Z0-9_\s-]+',
        'cpu.5min': r'\s*[x0-9a-f-]+\s+[x0-9a-f-]+\s+[0-9\.]+%\s+[0-9\.]+%\s+([0-9\.]+%)\s+[a-zA-Z0-9_\s-]+',
        'cpu.process': r'\s*[0-9a-fx-]+\s+[0-9_a-fx-]+\s+[0-9\.]+%\s+[0-9\.]+%\s+[0-9\.]+%\s+([a-zA-Z0-9_\s-]+)'
    }
}

regex_tags = {
    'asa': ['cpu.pc', 'cpu.thread', 'cpu.5sec', 'cpu.1min',
              'cpu.5min', 'cpu.process']
}

parsergen.extend(show_cmds=show_cmds, regex_ext=regex, regex_tags=regex_tags)


#attrValPairsToParse = [('cpu.process', 'vpnfol_thread_unsent')]
# attrValPairsToParse = [('cpu.process', 'pm_timer_thread')]
attrValPairsToParse = [('cpu.process', 'ARP Thread')]
# attrValPairsToParse = [('cpu.process', 'DATAPATH-0-1681')]

pgfill = parsergen.oper_fill(
    asa, 'show_cpu_sorted', attrvalpairs = attrValPairsToParse,
    refresh_cache=True, regex_tag_fill_pattern='cpu')
pgfill.parse()

pprint(parsergen.ext_dictio)

