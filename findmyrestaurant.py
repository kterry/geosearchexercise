#!/usr/bin/env python

import argparse
import sys
from ConfigParser import SafeConfigParser

from geofinder import GeoFinder

DEFAULT_DISTANCE = 500.0


parser = argparse.ArgumentParser(description="Find My Restaurant."
    " Find all the restaurants within a given distance of any particular UK"
    " and produce a list of restaurant names and the distance from the given postcode.")

parser.add_argument("postcode", 
                    action="store", 
                    help="Postal code.")
parser.add_argument("-d", "--distance",
                    type=float,
                    action="store", 
                    default=DEFAULT_DISTANCE, 
                    help="Max distance on metres from the given postal code. "
                    "Default: {}".format(DEFAULT_DISTANCE))
parser.add_argument("-p", "--pretty-print",
                    action="store_true",  
                    help="Pretty print output")

def main():
    # Get arguments 
    args = parser.parse_args()

    # Get application configuration
    config = SafeConfigParser()
    config.read("geofinder.ini")

    postcodes_filepath = config.get("files", "postcodes")
    restaurants_filepath = config.get("files", "restaurants")

    # create a GeoFinder instance loading files data
    geo_finder = GeoFinder.load(postcodes_filepath, restaurants_filepath)

    try:
        # get list of tuples (distance, restaurant name)
        restaurants = geo_finder.get_nearby_restaurant(args.postcode, args.distance)

    except ValueError:
        err_message = "Given postcode not found"
        sys.exit(err_message)

    # order by distance and print restaurants
    restaurants = sorted(restaurants)
   
    if args.pretty_print:
        print "{:20}\t{}".format("RESTAURANT", "DISTANCE (m)")

    
    for distance, name in restaurants:
        if args.pretty_print:
            print "{:20}\t{:.0f}".format(name, distance)
        else:
            print "{}\t{:.0f}".format(name, distance)

  
if __name__ == '__main__':
    main()