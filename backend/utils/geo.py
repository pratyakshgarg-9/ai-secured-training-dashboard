from geopy.distance import geodesic

def geo_risk(last_location, new_location, hours):
    if not last_location or not new_location:
        return 0.0

    try:
        # Accept BOTH dict and list formats safely
        if isinstance(last_location, list):
            last_lat, last_lon = last_location
        else:
            last_lat = last_location.get("latitude")
            last_lon = last_location.get("longitude")

        if isinstance(new_location, list):
            new_lat, new_lon = new_location
        else:
            new_lat = new_location.get("latitude")
            new_lon = new_location.get("longitude")

        if None in (last_lat, last_lon, new_lat, new_lon):
            return 0.0

        distance_km = geodesic((last_lat, last_lon), (new_lat, new_lon)).km
        speed = distance_km / max(hours, 0.1)

        if speed > 900:
            return 1.0

        return min(speed / 900, 1.0)

    except Exception as e:
        print("Geo risk error:", e)
        return 0.0
