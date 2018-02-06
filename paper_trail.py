import urllib.request
import configparser
import json

def get_config(config_file):
    c = configparser.ConfigParser()
    c.read(config_file)
    return {s:dict(c.items(s)) for s in c.sections()}

def fetch_transloc_json(config):
    c = config['Transloc']
    url = ("https://transloc-api-1-2.p.mashape.com/arrival-estimates.json?" +
    'agencies=' + c['agency'] + '&callback=call' +
    '&routes=' + c['route_id'] +
    '&stops=' + c['home_stop'])
    headers = {
            'X-Mashape-Key': c['api_key'],
            'Accept': 'application/json'
            }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return f.read()
