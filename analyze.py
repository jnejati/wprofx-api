#!/usr/bin/env python3.5
import os
import json
import shutil
import subprocess
import time

_experiment_dir = '/home/jnejati/trace_files/chrome_64_a7_on_a7_a7net'
_experiment_dir = '/home/jnejati/trace_files/chrome_44_a4_on_a7_a7net'
_experiment_dir = '/home/jnejati/trace_files/test'
_all_dirs = os.listdir(_experiment_dir)
_all_dirs.sort()
_exclude_list = []
working_dirs = [x for x in _all_dirs if x not in _exclude_list]
node = '/home/jnejati/.nvm/versions/node/v12.10.0/bin/node'
for _site_dir in working_dirs:
    _site_dir = os.path.join(_experiment_dir, _site_dir)
    _runs = [x for x in os.listdir(_site_dir) if x.startswith('run')]
    for _run_no in _runs:
        _run_dir = os.path.join(_site_dir, _run_no)
        _analysis_dir = os.path.join(_run_dir, 'analysis')
        if os.path.isdir(_analysis_dir):
            for root, dirs, l_files in os.walk(_analysis_dir):
                for f in l_files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        else:
            os.makedirs(_analysis_dir)
        _trace_dir = os.path.join(_run_dir, 'trace')
        for _file in os.listdir(_trace_dir):
            _trace_file = os.path.join(_trace_dir, _file)
            _output_file = os.path.join(_analysis_dir, _file.split('.trace')[0] + '.out')
            print('Analyzing ' + _run_no + ' site: ' + _site_dir)
            print(node, _trace_file, _output_file)
            subprocess.call([node, './wprofx.js', _trace_file, _output_file], timeout = 300)
    with open('analyzed_sofar.txt', 'a') as _a:
        _a.write(_site_dir.split('/')[-1] + '\n')
