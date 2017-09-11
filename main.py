#!/usr/bin/python3

import json
import requests
import configparser
from extensions.chartjs.ChartJsGenerator import ChartJsGenerator


config = configparser.ConfigParser()
config.read('config.ini')

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
