import gpxpy.geo

def geoDistance(lat1, lng1, lat2, lng2):
    return gpxpy.geo.haversine_distance(lat1, lng1, lat2, lng2)

def geoDistanceString(dist):
    if dist > 1000:
        return str(int(dist / 1000)) + "km"
    return "~" + str(int(dist)) + "m"