# SC

sport=climbing (sc) is a script that will grab all indoor and outdoor climbing walls near you.

<img width="513" height="487" alt="image" src="https://github.com/user-attachments/assets/94a2ef7f-a2d6-46f0-ba5f-23593d95fd1d" />

## Technical deets

It uses OpenStreetMaps data (which is also mostly submitted by me lol) to grab
all the locations of climbs within a given `--radius` (defaulting to 15 miles).

Distances to each location are calculated naively with the Haversine formula to
save me calling yet another API.

It uses a locally hosted Overpass instance to query all the location data.
You can run this yourself with

```
docker run -d \
  -e OVERPASS_MODE=clone \
  -e OVERPASS_PLANET_URL=https://download.geofabrik.de/europe/great-britain/wales-latest.osm.bz2 \
  -p 8082:80 \
  --name overpass_local \ 
  wiktorn/overpass-api
```

But beware, it takes a day on my machine to import all the data from
OpenStreetMaps.

There is a free version of this API hosted on the web but it's so slow and
times out all the time that it's probably not worth it.
