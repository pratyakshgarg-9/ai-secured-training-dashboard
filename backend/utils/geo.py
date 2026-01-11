from geopy.distance import geodesic

def _get_lat_lon(obj):
    if not obj:
        return None, None

    # list/tuple
    if isinstance(obj, (list, tuple)) and len(obj) >= 2:
        return obj[0], obj[1]

    # dict
    if isinstance(obj, dict):
        lat = obj.get("latitude", obj.get("lat"))
        lon = obj.get("longitude", obj.get("lon"))
        return lat, lon

    return None, None


def geo_risk(last_location, new_location, hours):
    if not last_location or not new_location:
        return 0.0

    try:
        last_lat, last_lon = _get_lat_lon(last_location)
        new_lat, new_lon = _get_lat_lon(new_location)

        if None in (last_lat, last_lon, new_lat, new_lon):
            return 0.0

        distance_km = geodesic((last_lat, last_lon), (new_lat, new_lon)).km
        speed = distance_km / max(hours, 0.1)

        # impossible travel threshold
        if speed > 900:
            return 1.0

        return min(speed / 900, 1.0)

    except Exception as e:
        print("Geo risk error:", e)
        return 0.0
