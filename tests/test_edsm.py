import unittest

from edsm import traffic
from edsm import systems_radius

class TrafficTest(unittest.TestCase):
    def test_bad_name_Wawawa(self):
        self.assertRaises(Exception, traffic, 'Wawawa')

    def test_traffic_Sol(self):
        json = traffic('Sol')

        self.assertEqual(27, json['id'])
        self.assertEqual(10477373803, json['id64'])
        self.assertEqual('Sol', json['name'])
        self.assertEqual('https://www.edsm.net/en/system/id/27/name/Sol', json['url'])

        self.assertEqual('J. Calvert (Joshua)', json['discovery']['commander'])
        self.assertEqual('2014-11-18 18:21:43', json['discovery']['date'])

        self.assertIs(type(json['traffic']), dict)
        self.assertIs(type(json['traffic']['total']), int)
        self.assertIs(type(json['traffic']['week']), int)
        self.assertIs(type(json['traffic']['day']), int)
        self.assertIs(type(json['breakdown']), dict)
        
    def test_traffic_Warkawa(self):
        json = traffic('Warkawa')

        self.assertEqual(14026, json['id'])
        self.assertEqual(18261798168017, json['id64'])
        self.assertEqual('Warkawa', json['name'])
        self.assertEqual('https://www.edsm.net/en/system/id/14026/name/Warkawa', json['url'])

        self.assertEqual('sutex', json['discovery']['commander'])
        self.assertEqual('2015-01-05 11:13:31', json['discovery']['date'])

        self.assertIs(type(json['traffic']), dict)
        self.assertIs(type(json['traffic']['total']), int)
        self.assertIs(type(json['traffic']['week']), int)
        self.assertIs(type(json['traffic']['day']), int)
        self.assertIs(type(json['breakdown']), dict)

    def test_traffic_warkawa_lowercase(self):
        json = traffic('warkawa')

        self.assertEqual(14026, json['id'])
        self.assertEqual(18261798168017, json['id64'])
        self.assertEqual('Warkawa', json['name'])
        self.assertEqual('https://www.edsm.net/en/system/id/14026/name/Warkawa', json['url'])

        self.assertEqual('sutex', json['discovery']['commander'])
        self.assertEqual('2015-01-05 11:13:31', json['discovery']['date'])

        self.assertIs(type(json['traffic']), dict)
        self.assertIs(type(json['traffic']['total']), int)
        self.assertIs(type(json['traffic']['week']), int)
        self.assertIs(type(json['traffic']['day']), int)
        self.assertIs(type(json['breakdown']), dict)


class SystemsRadiusTest(unittest.TestCase):
    def test_bad_name_Wawawa(self):
        self.assertRaises(Exception, systems_radius, 'Wawawa')

    def test_systems_radius_Warkawa_8(self):
        json = systems_radius('Warkawa', 8)

        distance_by_name = {system['name'] : system['distance'] for system in json}
        self.assertEqual(distance_by_name['Warkawa'], 0)
        self.assertEqual(distance_by_name['Aulendiae'], 6.89)

        self.assertNotIn('Sol', json)
