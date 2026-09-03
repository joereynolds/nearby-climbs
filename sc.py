#!/usr/bin/env python

import argparse
import json
import math
import urllib.request


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Gets straight-line distance between two lat/lon pairs in miles"""
    R = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c
    distance_miles = distance_km * 0.621371

    return distance_miles

location_url = "https://ipinfo.io/json"
# overpass_url = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
overpass_url = "http://localhost:8080/api/interpreter"

parser = argparse.ArgumentParser(
    prog="sc",
    description="Find local climbs",
)

parser.add_argument(
    '-l',
    '--limit',
    help="How many climbs to return",
    type=int,
    default=20,
)

parser.add_argument(
    '-r',
    '--radius',
    help="The search radius from your location in miles",
    type=int,
    default=15
)

parser.add_argument('-v', '--verbose')

args = parser.parse_args()

location_data = json.loads(urllib.request.urlopen(location_url).read())

# this isn't my real location, creeps
location_data = {"loc": "53.193458, -2.883632"}

lat, lon = map(float, location_data["loc"].split(","))

lat_adjustment = args.radius / 69
lon_adjustment = args.radius / (69 * math.cos(math.radians(lat)))

min_lat, max_lat = round(lat - lat_adjustment, 3), round(lat + lat_adjustment, 3)
min_lon, max_lon = round(lon - lon_adjustment, 3), round(lon + lon_adjustment, 3)

bbox = f"({min_lat},{min_lon},{max_lat},{max_lon})"

query = f"""
[out:csv(::type, ::id, ::lat, ::lon, "name"; false; ",")];
(
  nwr["sport"="climbing"][name]{bbox};
);
out center {args.limit};
"""

data = query.encode("utf-8")

request = urllib.request.Request(overpass_url, data=data)

with urllib.request.urlopen(request) as response:

    results = response.read().decode("utf-8").strip().split("\n")

    for line in results:
        osm_type, osm_id, osm_lat, osm_lon, name = line.split(",")

        try:
            distance = calculate_distance(
                lat, lon,
                float(osm_lat), float(osm_lon)
            )
        except ValueError:
            distance = "Unknown"

        url = f"https://www.openstreetmap.org/{osm_type}/{osm_id}"
        print(f"{name[0:34]:<35} ({int(distance)} miles away) ({url})")

# Improvements:
# take a --location param
#
# Cache each call and save in XDG_DATA_HOME.
# For example:
# sc --radius 10
# result would get cached and saved in XDG_DATA_HOME so we don't hammer the API
#
# Link the OSM url or something
