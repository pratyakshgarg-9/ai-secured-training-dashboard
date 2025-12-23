from geopy.distance import geodesic

class GeoVelocityDetector:
    def score(self, last_loc, new_loc, time_gap_hours):
        distance = geodesic(last_loc, new_loc).km
        velocity = distance / max(time_gap_hours, 0.1)
        if velocity > 900:
            return 1.0
        elif velocity > 300:
            return 0.7
        else:
            return 0.2
