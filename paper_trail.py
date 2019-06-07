#!/usr/bin/env python3

import urllib.request
import configparser
import json
import dateutil.parser
from dateutil import tz
import datetime as dt

def get_config(config_file = 'config.ini'):
    c = configparser.ConfigParser()
    c.read(config_file)
    return {s:dict(c.items(s)) for s in c.sections()}


#TODO
def url_constructor(config):
    c = config['Transloc']
    geo_area = f"{config['User']['latitude']}%2C{config['User']['longitude']}%7C{radius}"
    url = ("https://transloc-api-1-2.p.rapidapi.com/agencies.json?" +
    "geo_area=" + geo_area +
    "&callback=call")
    headers={
        "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com",
        "X-RapidAPI-Key": c['api_key']
    }


def fetch_agencies(config, latitude = 29.64176, longitude = -82.34500, radius = 1000):
    c = config['Transloc']
    geo_area = f"{config['User']['latitude']}%2C{config['User']['longitude']}%7C{radius}"
    url = ("https://transloc-api-1-2.p.rapidapi.com/agencies.json?" +
    "geo_area=" + geo_area +
    "&callback=call")
    headers={
        "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com",
        "X-RapidAPI-Key": c['api_key']
    }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())


def fetch_stops(config, radius = 10):
    c = config['Transloc']
    geo_area = f"{config['User']['latitude']}%2C{config['User']['longitude']}%7C{radius}"
    url = ("https://transloc-api-1-2.p.rapidapi.com/stops.json?" +
    "callback=call" +
    "&agencies=" + c['agency'] +
    "&geo_area=" + geo_area
    )
    headers={
        "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com",
        "X-RapidAPI-Key": c['api_key']
    }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())

def fetch_routes(config, radius = 10):
    "https://transloc-api-1-2.p.rapidapi.com/routes.json?"
    c = config['Transloc']
    geo_area = f"{config['User']['latitude']}%2C{config['User']['longitude']}%7C{radius}"
    url = ("https://transloc-api-1-2.p.rapidapi.com/routes.json?" +
    "callback=call" +
    "&agencies=" + c['agency'] +
    "&geo_area=" + geo_area
    )
    headers={
        "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com",
        "X-RapidAPI-Key": c['api_key']
    }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())

def writefile(json_return, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_return, indent = 4))

def refresh_transloc_cache():
    file_pairs = [[], []]
    [writefile(f[0], f[1]) for f in file_pairs]



def display_stops(stops_data):
    stops_data = stopds_data['data']
    return True;


def fetch_arrival_estimates(config, routes, stops, spacer = "%2C"):
    c = config['Transloc']
    url = ("https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json?" +
    'routes=' + spacer.join(routes) +
    '&agencies=' + c['agency'] + '&callback=call' +
           '&stops=' + spacer.join(stops))
    headers = {
            'X-Mashape-Key': c['api_key'],
            'Accept': 'application/json'
            }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())

def bus_to_get_to(current_location, destination_stop_id):
    # Take current location as latlong or stop?
    # Call to Google API?
    return 1


def calc_time_transloc(jsn, arvl_num = 0):
    d_now = dt.datetime.now()
    arvl = jsn['data'][0]['arrivals'][arvl_num]['arrival_at']
    d_arvl = dateutil.parser.parse(arvl).replace(tzinfo=None)
    d_dif = d_arvl - d_now
    return d_arvl, d_dif

def calc_leave_time(jsn, c):
    missed = 0
    walk_time = float(c['User']['walk_time'])
    d_arvl, d_dif = calc_time_transloc(jsn)
    if d_dif.seconds/60 - walk_time < 0:
        missed = 1
        print('You\'ll likely miss the {} bus'.format(d_arvl.strftime('%H:%M')))
        d_arvl, d_dif = calc_time_transloc(jsn, 1)
    tt_leave = round(d_dif.seconds/60 - walk_time, 2)
    return tt_leave, d_arvl


def process_arrival_estimates(arrivals, routes, stops):
    now = dt.datetime.now()

    def localize_utc(utc_dt):
        return utc_dt.astimezone(tz=tz.tzlocal())
        # return utc_dt.replace(tzinfo=dt.timezone.utc).astimezone(tz=tz.tzlocal())


    last_updated = localize_utc(dateutil.parser.parse(arrivals['generated_on']))

    for stop_data in arrivals['data']:
        print(f"Arrivals for stop: {stops[stop_data['stop_id']]}")

        for arrival in stop_data['arrivals']:
            arrival_time = dateutil.parser.parse(arrival['arrival_at']).replace(tzinfo=None)
            time_to_arrival = arrival_time - now
            print(f"Bus {routes[arrival['route_id']]} will arrive in {round(time_to_arrival.seconds / 60)} minutes, at {arrival_time.strftime('%H:%M')}")

        print("\n\n")

    print(f"Last updated at {last_updated.strftime('%H:%M')}\n\n")


def main():
    config = get_config()

    # {'transloc id' : 'common name' }
    routes = {
        '4001170' : '1',
        '4001150' : '12'
    }
    stops = {
        '4091646' : 'Mt Vernon Apts Westbound',
        '4191516' : 'Eastbound Archer RD @ Farside SW 23rd DR'
    }

    arrivals = fetch_arrival_estimates(config, routes.keys(), stops.keys())

    process_arrival_estimates(arrivals, routes, stops)


if __name__ == '__main__':
    main()
