#!/usr/bin/env python3.5
__author__ = 'jnejati'

#import experiments
import json
import os
from urllib.parse import urlparse
import time
import urllib.request
import urllib.response
import io
import subprocess
import logging
import timeit

def main():
    start = timeit.default_timer()
    exp = 'chrome_64_a7_2010pages'
    exp = 'chrome_44_a4_on_a7_a7net'
    #exp = 'chrome_53_a6_on_a7_a7net'
    #exp = 'chrome_47_a5_on_a7_a7net'
    #exp = 'chrome_64_a7_on_a7_a7net'
    _path =  '../trace_files'
    _path = os.path.join(_path, exp)
    node = '/home/jnejati/.nvm/versions/node/v12.10.0/bin/node'
    with open('./config/testsites.txt') as _sites:
        for i in range(25):
            next(_sites)
        for _site in _sites:
            _site = _site.strip() + '/'
            print('Navigating to: ' + _site)
            _domain = _site.split('//')[-2]
            if ':80' in _domain:
                _domain.replace(':80','')
            print('Saving as: ', _domain)
            _site_data_folder = os.path.join(_path, _domain)
            if not os.path.isdir(_site_data_folder):
                os.mkdir(_site_data_folder)
            print('Starting runs:')
            for run_no in range(3):
                _run_data_folder = os.path.join(_site_data_folder, 'run_' + str(run_no))
                if not os.path.isdir(_run_data_folder):
                    os.mkdir(_run_data_folder)
                    _subfolders = ['trace', 'analysis']
                    for folder in _subfolders:
                        os.mkdir(os.path.join(_run_data_folder, folder))
                os.system('pkill node')
                time.sleep(5)
                _trace_folder = os.path.join(_run_data_folder, 'trace')
                _trace_file = os.path.join(_trace_folder, str(run_no) + '_' + _domain)
                logging.info(_trace_file)
                try:
                    _node_cmd = [node, 'traceGatherer.js', _site ,  _trace_file]
                    subprocess.call(_node_cmd, timeout = 300)
                except subprocess.TimeoutExpired:
                    print("Timeout:  ", _site, run_no)
                time.sleep(5)
    stop = timeit.default_timer()
    logging.info(100*'-' + '\nTotal time: ' + str(stop -start)) 
if __name__ == '__main__':
    main()
