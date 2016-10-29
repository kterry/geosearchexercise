from collections import namedtuple
import math
import csv

Coordinates = namedtuple("Coordinates",
    ["latitude",  # latitude in degrees
     "longitude"  # latitude in degrees
    ])

class GeoFinder(object):

    def __init__(self):
        self._postcodes = {}           # postcode - Coordinates
        self._postcodeRestaurants = {} # postcode - list of restaurants


    def add_postcode(self, postcode, latitude, longitude):
        postcode = self._normalize_postcode(postcode)
        self._postcodes[postcode] = Coordinates(latitude, longitude)

    def add_restaurant(self, restaurant, postcode):
        postcode = self._normalize_postcode(postcode)

        if postcode in self._postcodeRestaurants: 
            self._postcodeRestaurants[postcode].append(restaurant)
        else:
            self._postcodeRestaurants[postcode] = [restaurant]

    def get_nearby_restaurant(self, postcode, maxDistance):
        """
        Returns a list of tuples with the distance of the restaurant from the 
        given postcode and the restaurant name.

        Throws a ValueError exception when the postcode is invalid.
        """
        postcode = self._normalize_postcode(postcode)
        if postcode not in self._postcodes:
            raise ValueError("Invalid postcode")

        nearby_restaurants = []
        postcode_coords = self._postcodes[postcode]

        for res_postcode, restaurants in self._postcodeRestaurants.items():
            res_coords = self._postcodes[res_postcode]
            distance = haversine_distance(postcode_coords, res_coords)

            if distance <= maxDistance:
                for restaurant in restaurants:
                    nearby_restaurants.append( (distance, restaurant) )

        return nearby_restaurants

    @classmethod
    def load(cls, postcodes_filepath, restaurants_filepath):

        geo_finder = cls()

        with open(postcodes_filepath, 'rb') as f:
            reader = csv.reader(f)

            # Postcode, east (m), north (m), latitude(N), longitude(E)
            for row in reader:
                #if the row has no the expected data ignore it
                if len(row) != 5:
                    continue

                try:
                    postcode = row[0].strip()
                    lat = float(row[3])
                    lon = float(row[4])

                    geo_finder.add_postcode(postcode, lat, lon)
                except:
                    #if the row data is not valid, ignore it
                    pass

        with open(restaurants_filepath, 'rb') as f:
            reader = csv.reader(f)

            # Name, Postcode
            for row in reader:
                #if the row has no the expected data ignore it
                if len(row) != 2:
                    continue

                try:
                    geo_finder.add_restaurant(row[0].strip(), row[1].strip())
                except:
                    #if the row data is not valid, ignore it
                    pass

        return geo_finder

    def _normalize_postcode(self, postcode):
        return postcode.upper().replace(" ", "").replace("\t", "")


def haversine_distance(coordinates1, coordinates2):
    """
    Uses 'haversine' formula to calculate the distance between to points
    (see http://www.movable-type.co.uk/scripts/latlong.html)
    """

    # earth radius on metres
    R = 6371e3

    # lat, long in radians
    lat1 = coordinates1.latitude * (math.pi/180)
    lat2 = coordinates2.latitude * (math.pi/180)
    lon1 = coordinates1.longitude * (math.pi/180)
    lon2 = coordinates2.longitude * (math.pi/180)

    # a = sin(lat_delta/2)^2 + cos(lat1) * cos(lat2) * sin(lon_delta)^2
    lat_delta = lat2 - lat1
    lon_delta = lon2 - lon1
    s1 = math.sin(lat_delta/2)
    s2 = math.sin(lon_delta/2)

    a = (s1 * s1) + (math.cos(lat1) * math.cos(lat2) * s2 * s2)

    # c = 2 * atan2(sqrt(a), sqrt(1-a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c

    return d
