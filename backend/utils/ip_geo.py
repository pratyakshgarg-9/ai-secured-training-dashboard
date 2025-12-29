import requests

def ip_to_geo(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = res.json()
        if data["status"] != "success":
            return None

        return {
            "country": data["country"],
            "city": data["city"],
            "lat": data["lat"],
            "lon": data["lon"]
        }
    except:
        return None
