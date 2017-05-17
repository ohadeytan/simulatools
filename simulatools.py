from traces import *
from policies import *
import fire
import urllib
import os
import csv
import json
from subprocess import call
import subprocess
from pyhocon import ConfigFactory
from pyhocon import ConfigTree
from pyhocon import HOCONConverter
from enum import Enum
from pprint import pprint
import matplotlib.pyplot as plt
import pickle

with open('conf.json') as conf_file:
    local_conf = json.load(conf_file)

class Admission(Enum):
    ALWAYS = 'Always'
    TINY_LFU = 'TinyLfu'

def single_run(policy, trace, size=4, changes={}, name=None, save=True, reuse=False, verbose=False):
    name = name if name else policy
    policy = Policy[policy]
    trace = Trace[trace]
    if 0 < size < 9:
        size = trace.typical_caches()[size-1]
    conf_path = local_conf['caffeine_root'] + 'simulator' + os.sep + 'src' + os.sep + 'main' + os.sep + 'resources' + os.sep
    conf_file = conf_path + 'application.conf'
    working_path = os.getcwd() + os.sep + 'csvs' + os.sep;
    if not os.path.exists(working_path):
        os.makedirs(working_path)
    run_simulator = './gradlew simulator:run'
    if os.path.exists(conf_file):
        conf = ConfigFactory.parse_file(conf_file)
    else:
        conf = ConfigFactory.parse_string("""
                                          caffeine {
                                            simulator {
                                            }
                                          }
                                          """)
    simulator = conf['caffeine']['simulator']
    simulator.put('files.paths', [ local_conf['caffeine_root'] + 'simulator/src/main/resources/com/github/benmanes/caffeine/cache/simulator/parser/'.replace('/',os.sep) + trace.format() + os.sep + trace.file() ])
             
    simulator.put('files.format', trace.value['format'])
    simulator.put('maximum-size', size)
    simulator.put('policies', [ policy.value ])
    simulator.put('admission', [ Admission.ALWAYS.value ])
    simulator.put('report.format', 'csv')
    simulator.put('report.output', working_path + '{}-{}-{}.csv'.format(trace.name,size,name))

    for k,v in changes.items():
        simulator.put(k,v)

    with open(conf_file, 'w') as f:
        f.write(HOCONConverter.to_hocon(conf))
    if not reuse or not os.path.isfile(simulator['report']['output']):
        call(run_simulator, shell = True, cwd = local_conf['caffeine_root'], stdout = subprocess.DEVNULL if not verbose else None)
    with open(simulator['report']['output'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        result = float(next(reader)['Hit rate'])
    if not save:
        os.remove(simulator['report']['output'])
    return result

def download_single_trace(trace, path=None):
        if not path:
            path = local_conf['caffeine_root'] + \
                   'simulator/src/main/resources/com/github/benmanes/caffeine/cache/simulator/parser'.replace('/',os.sep) 
        if path[-1] != os.sep:
            path += os.sep
        if not os.path.exists(path + trace.format()):
            os.makedirs(path + trace.format())
        print('Downloading ' + trace.name + '...')
        urllib.request.urlretrieve(trace.url() + '?dl=1', path + trace.format() + os.sep + trace.file())
        print(trace.name + ' downloaded')

def parse_traces(traces):
    if not traces:
        return [trace for trace in Trace]
    if type(traces) == str:
        traces = [ traces ]
    if type(traces) == list:
        return [ Trace[trace] for trace in traces ]
    return []

def rf_rank(trace, size):
    lru = single_run('lru', trace.name, size, save=True, reuse=True)
    lfu = single_run('lfu', trace.name, size, save=True, reuse=True)
    opt = single_run('opt', trace.name, size, save=True, reuse=True)
    return (lru-lfu)/opt 

class Tools(object):

    def download_traces(self, traces=None, path=None):
        """ 
        Download all traces to the given path, if the path is empty - download to caffeine resources path.
        Each trace placed into a subdirectory with the format name.
        """
        traces = parse_traces(traces)
        for trace in traces:
            download_single_trace(trace, path)

    def list_traces(self):
        """
        Print all the avaliable traces.
        """
        print('Avaliable traces are:')
        print('-'*83)
        print('|{:^15}|{:^65}|'.format('Trace Name','Typical Cache Sizes'))
        print('-'*83)
        for trace in Trace:
            print('|{:^15}|{:^65}| '.format(trace.name,str(trace.typical_caches())[1:-1]))
        print('-'*83)

    def run(self, policy, trace, size=4, changes={}, name=None, save=True, reuse=False, verbose=False):
        res = single_run(policy, trace, size, changes, name, save, reuse, verbose)
        print('The hit rate of {} on {} with cache size of {} is: {}%'
                .format(name if name else policy, trace, size if size > 8 else Trace[trace].typical_caches()[size-1], res))

    def battle(self, policy1, policy2, changes1={}, changes2={}, name1=None, name2=None, save=True, reuse=False, verbose=False, rfo=False):
        self.compare(policies=[policy1, policy2], changes=[changes1, changes2], names=[name1, name2], save=save, reuse=reuse, verbose=verbose, rfo=rfo)

    def compare(self, policies, changes=None, names=None, save=True, reuse=False, verbose=False, rfo=False):
        if not changes:
            changes = [{}]*len(policies)
        if not names:
            names = policies
        policies_wins = [0]*len(policies)

        columns = 3 + len(policies) + (1 if rfo else 0)
        line = ' ' + '-'*(16 * columns - 1)
        text ='|' + '{:^15}|'*columns 
        print(line)
        headers = ['Trace','Cache Size'] + (['(LRU-LFU)/OPT'] if rfo else []) 
        print(text.format(*headers, *names, 'Difference'))
        print(line)

        for trace in Trace:
            for size in range(1,1+8):
                policies_hr = [ single_run(policy, trace.name, size, change, name, save, reuse, verbose) \
                                for policy, change, name in zip(policies, changes, names)]
                texts = [trace.name, trace.typical_caches()[size-1]] + (['{:2.2f}'.format(rf_rank(trace, size))] if rfo else []) + \
                        ['{:2.2f}%'.format(policy_hr) for policy_hr in policies_hr] + ['{:2.2f}%'.format(max(policies_hr)-min(policies_hr))]
                min_index = policies_hr.index(min(policies_hr))
                max_index = policies_hr.index(max(policies_hr))
                
                offset = 2 + (1 if rfo else 0)
                texts[offset + min_index] = ''
                texts[offset + max_index] = '\N{CHECK MARK} ' + texts[offset + max_index] 

                if min_index == max_index:
                    for i in range(len(policies_hr)):
                        texts[offset + i] = ''

                print(text.format(*texts))

                if min_index != max_index:
                    policies_wins[max_index] += 1

        print(line)
        print(text.format(*(['']*(1 + (1 if rfo else 0))),'Total Wins:', *policies_wins, ''))
        print(line)

if __name__ == '__main__':
    fire.Fire(Tools)
