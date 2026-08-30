#!/usr/bin/env python

import json
import math
import urllib.request

location_url = "https://ipinfo.io/json"
overpass_url = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"

radius = 15.0
result_limit = 20

location_data = json.loads(urllib.request.urlopen(location_url).read())

lat, lon = map(float, location_data["loc"].split(","))

lat_adjustment = radius / 69
lon_adjustment = radius / (69 * math.cos(math.radians(lat)))

min_lat, max_lat = round(lat - lat_adjustment, 3), round(lat + lat_adjustment, 3)
min_lon, max_lon = round(lon - lon_adjustment, 3), round(lon + lon_adjustment, 3)

bbox = f"({min_lat},{min_lon},{max_lat},{max_lon})"

query = f"""
[out:csv("name"; false; "")][timeout:10];
(
  nwr["sport"="climbing"][name]{bbox};
);
out tags {result_limit};
"""

data = query.encode("utf-8")

request = urllib.request.Request(
    overpass_url,
    data=data,
)

with urllib.request.urlopen(request) as response:
    result = response.read().decode("utf-8").strip()
    print(result)

# Improvements:
# take a --limit param
# take a --radius param
# take a --location param
#
# Cache each call and save in XDG_DATA_HOME.
# For example:
# sc --radius 10
# result would get cached and saved in XDG_DATA_HOME so we don't hammer the API
#
# Link the OSM url or something

