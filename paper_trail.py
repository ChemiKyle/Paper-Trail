#!/usr/bin/env python3

import urllib.request
import configparser
import json
import dateutil.parser
import datetime as dt

def get_config(config_file):
    c = configparser.ConfigParser()
    c.read(config_file)
    return {s:dict(c.items(s)) for s in c.sections()}


def fetch_json_transloc(config):
    c = config['Transloc']
    url = ("https://transloc-api-1-2.p.mashape.com/arrival-estimates.json?" +
    'agencies=' + c['agency'] + '&callback=call' +
    '&routes=' + c['route_id'] +
    '&stops=' + c['stop_id'])
    headers = {
            'X-Mashape-Key': c['api_key'],
            'Accept': 'application/json'
            }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())


def calc_time_transloc(jsn):
    d_now = dt.datetime.now()
    arvl = jsn['data'][0]['arrivals'][0]['arrival_at']
    d_arvl = dateutil.parser.parse(arvl).replace(tzinfo=None)
    d_dif = d_arvl - d_now
    return d_arvl, d_dif


def main():
    walk_time = 3 # Time to get to the stop (minutes)
    c = get_config('config.ini')
    d_arvl, d_dif = calc_time_transloc(fetch_json_transloc(c))
    print("Nearest bus will arrive at {}".format(d_arvl.strftime('%H:%M')))
    print("Leave in {} minutes".format(round(d_dif.seconds/60 - walk_time, 2)))


if __name__ == '__main__':
    main()
