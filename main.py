#!/usr/bin/python3

import json, os, sys
import requests
import configparser
from pathlib import Path
from extensions.chartjs.ChartJsGenerator import ChartJsGenerator

script_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

if Path("/etc/pr0stats.ini").is_file():
    config.read('/etc/pr0stats.ini')
elif Path("/etc/pr0stats/config.ini").is_file():
    config.read("/etc/pr0stats/config.ini")
elif Path(script_path+"/config.ini").is_file():
    config.read(script_path+'/config.ini')
else:
    sys.stderr.write("Config-File not found.")
    sys.exit(1)

api = "https://pr0gramm.com/api/profile/info?name={}&flags=4".format(config['general']['username'])
resp = json.loads(requests.get(api).text)

if "sqlite" in config and config['sqlite'].getboolean('enabled'):
    from processors.sqlite import Processor
else:
    from processors.plain_file import Processor

processor = Processor(config)
processor.save_score(resp)

if "chartjs" in config and config["chartjs"].getboolean('enabled'):
    js_gen = ChartJsGenerator(config,processor)
    js_gen.generate()
