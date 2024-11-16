from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def getLatLong(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    loc = geolocator.geocode(address)
    if loc:
        return loc.latitude, loc.longitude
    else:
        return None

def getDistance(location1, location2):
    #convert address (locationx) to lat long
    latlong1 = getLatLong(location1)
    latlong2 = getLatLong(location2)
    if latlong1 is None:
        return f'Address {location1} not found.'
    if latlong2 is None:
        return f'Address {location2} not found.'
    distInMiles = geodesic(latlong1, latlong2).miles
    return distInMiles