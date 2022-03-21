import unittest
from xml.etree.ElementInclude import include

from edsm import System
from edsm import Systems

class SystemTest(unittest.TestCase):
    def test_traffic_Wawawa(self):
        # as of writing this, there are no systems in the game named 'Wawawa', 
        # so System.traffic should return an empty obj
        self.assertRaises(Exception, System.traffic, 'Wawawa')
        
    def test_traffic_Sol(self):
        d = System.traffic('Sol')

        self.assertIs(type(d), dict)

        self.assertEqual(27, d['id'])
        self.assertEqual(10477373803, d['id64'])
        self.assertEqual('Sol', d['name'])
        self.assertEqual('https://www.edsm.net/en/system/id/27/name/Sol', d['url'])

        self.assertEqual('J. Calvert (Joshua)', d['discovery']['commander'])
        self.assertEqual('2014-11-18 18:21:43', d['discovery']['date'])

        self.assertIs(type(d['traffic']), dict)
        self.assertIs(type(d['traffic']['total']), int)
        self.assertIs(type(d['traffic']['week']), int)
        self.assertIs(type(d['traffic']['day']), int)
        self.assertIs(type(d['breakdown']), dict)

    def test_traffic_sol_lowercase(self):
        d = System.traffic('sol')

        self.assertIs(type(d), dict)

        self.assertEqual(27, d['id'])
        self.assertEqual(10477373803, d['id64'])
        self.assertEqual('Sol', d['name'])
        self.assertEqual('https://www.edsm.net/en/system/id/27/name/Sol', d['url'])

        self.assertEqual('J. Calvert (Joshua)', d['discovery']['commander'])
        self.assertEqual('2014-11-18 18:21:43', d['discovery']['date'])

        self.assertIs(type(d['traffic']), dict)
        self.assertIs(type(d['traffic']['total']), int)
        self.assertIs(type(d['traffic']['week']), int)
        self.assertIs(type(d['traffic']['day']), int)
        self.assertIs(type(d['breakdown']), dict)

    def test_stations_Sol(self):
        d = System.stations('Sol')

        self.assertIs(type(d), dict)

        self.assertEqual(27, d['id'])
        self.assertEqual(10477373803, d['id64'])
        self.assertEqual('Sol', d['name'])
        self.assertEqual('https://www.edsm.net/en/system/stations/id/27/name/Sol', d['url'])

        self.assertIs(type(d['stations']), list)

        # asserts assuming there are more than 0 stations in the system (there are, as of writing).
        station = d['stations'][0]
        self.assertIn('id', station)
        self.assertIn('marketId', station)
        self.assertIn('type', station)
        self.assertIn('name', station)
        self.assertIn('distanceToArrival', station)
        self.assertIn('allegiance', station)
        self.assertIn('government', station)
        self.assertIn('economy', station)
        self.assertIn('secondEconomy', station)
        self.assertIn('haveMarket', station)
        self.assertIn('haveShipyard', station)
        self.assertIn('haveOutfitting', station)
        self.assertIn('otherServices', station)
        self.assertIn('controllingFaction', station)
        self.assertIn('updateTime', station)

    def test_stations_sol_lowercase(self):
        d = System.stations('sol')

        self.assertIs(type(d), dict)

        self.assertEqual(27, d['id'])
        self.assertEqual(10477373803, d['id64'])
        self.assertEqual('Sol', d['name'])
        self.assertEqual('https://www.edsm.net/en/system/stations/id/27/name/Sol', d['url'])

        self.assertIs(type(d['stations']), list)

        # asserts assuming there are more than 0 stations in the system (there are, as of writing).
        station = d['stations'][0]
        self.assertIn('id', station)
        self.assertIn('marketId', station)
        self.assertIn('type', station)
        self.assertIn('name', station)
        self.assertIn('distanceToArrival', station)
        self.assertIn('allegiance', station)
        self.assertIn('government', station)
        self.assertIn('economy', station)
        self.assertIn('secondEconomy', station)
        self.assertIn('haveMarket', station)
        self.assertIn('haveShipyard', station)
        self.assertIn('haveOutfitting', station)
        self.assertIn('otherServices', station)
        self.assertIn('controllingFaction', station)
        self.assertIn('updateTime', station)

    def test_stations_Warkawa(self):
        d = System.stations('Warkawa')

        self.assertIs(type(d), dict)

        self.assertEqual(14026, d['id'])
        self.assertEqual(18261798168017, d['id64'])
        self.assertEqual('Warkawa', d['name'])
        self.assertEqual('https://www.edsm.net/en/system/stations/id/14026/name/Warkawa', d['url'])

        self.assertIs(type(d['stations']), list)

        # asserts assuming there are more than 0 stations in the system (there are, as of writing).
        station = d['stations'][0]
        self.assertIn('id', station)
        self.assertIn('marketId', station)
        self.assertIn('type', station)
        self.assertIn('name', station)
        self.assertIn('distanceToArrival', station)
        self.assertIn('allegiance', station)
        self.assertIn('government', station)
        self.assertIn('economy', station)
        self.assertIn('secondEconomy', station)
        self.assertIn('haveMarket', station)
        self.assertIn('haveShipyard', station)
        self.assertIn('haveOutfitting', station)
        self.assertIn('otherServices', station)
        self.assertIn('controllingFaction', station)
        self.assertIn('updateTime', station)

    def test_market_Achali_Garratt_Ring(self):
        d = System.market('Achali', 'Garratt Ring')
        
        self.assertEqual(4532, d['id'])
        self.assertEqual(3657332462314, d['id64'])
        self.assertEqual('Achali', d['name'])
        self.assertEqual(3230886400, d['marketId'])
        self.assertEqual(7821, d['sId'])
        self.assertEqual('Garratt Ring', d['sName'])
        
        self.assertIn('commodities', d)

    def test_factions_Warkawa_showHistory_option(self):
        d = System.factions('Warkawa', showHistory = 1)

        # tests for constants (id, id64, name) so we know it's found the right system

        self.assertIn('controllingFaction', d)
        self.assertIn('factions', d)

        for faction in d['factions']:
            self.assertIn('influenceHistory', faction)


class SystemsTest(unittest.TestCase):
    def test_sphere_systems_Alcor_all_options(self):
        d = Systems.sphere_systems(
                'Alcor', 
                20,
                showId = 1,
                showCoordinates = 1,
                showPermit = 1,
                showInformation = 1,
                showPrimaryStar = 1,
                includeHidden = 1
        )

        for system in d:
            self.assertIs(type(system), dict)

        # assuming there is at least 1 object returned 
        # (there are, as of writing (and there should be, for a long while))
        system = d[0]
        self.assertIn('distance', system)
        self.assertIn('bodyCount', system)
        self.assertIn('name', system)
        self.assertIn('id', system)
        self.assertIn('id64', system)

        self.assertIn('coords', system)
        self.assertIs(type(system['coords']), dict)

        for coord in system['coords']:
            self.assertIs(type(system['coords'][coord]), float)

        self.assertIn('information', system)
        self.assertIn('primaryStar', system)


"""
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
"""
