import unittest
import geofinder

class GeoFinderTestCase(unittest.TestCase):

    def test_distance_self(self):
        coords = geofinder.Coordinates(0, 0)
        self.assertEqual(geofinder.haversine_distance(coords, coords), 0.0)

    def test_distance_other(self):
        coords_bath = geofinder.Coordinates(51.379050, -2.359896)
        coords_bristol = geofinder.Coordinates(51.453259, -2.586047)
        distance = geofinder.haversine_distance(coords_bath, coords_bristol)

        # distance ~ 17730 m 
        self.assertLess(distance, 17740)
        self.assertGreater(distance, 17720)

    def test_restaurants_nearby(self):
        finder = geofinder.GeoFinder()

        finder.add_postcode("BA0 0XX", 51.379050, -2.359896)
        finder.add_postcode("BS0 0XX", 51.453259, -2.586047)
        finder.add_postcode("CB0 0XX", 52.210604, 0.120672)

        finder.add_restaurant("Bath Burguers", "BA0 0XX")
        finder.add_restaurant("Bath Noodles", "BA0 0XX")
        finder.add_restaurant("Bristol Tacos", "BS0 0XX")
        finder.add_restaurant("Cambridge Grill", "CB0 0XX")

        self.assertEqual(self._get_names(finder.get_nearby_restaurant("CB0 0XX", 1000)), 
                         ["Cambridge Grill"])

        self.assertEqual(self._get_names(finder.get_nearby_restaurant("BA0 0XX", 20000)), 
                         ["Bath Burguers", "Bath Noodles", "Bristol Tacos"])

    def _get_names(self, restaurants):
        return [ res[1] for res in restaurants ]


if __name__ == '__main__':
    unittest.main(verbosity=2)
