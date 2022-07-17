import unittest

import json

from edsm.models import Traffic
from edsm.models import Systems
from edsm.models import System

#TODO: finish Traffic test
class TrafficTest(unittest.TestCase):
    def test_Traffic_Sol(self):
        t = Traffic('Sol')
        t.update()

        self.assertIs(type(t.dict), dict)

class SystemsTest(unittest.TestCase):
    with open('tests/api_sphere_systems.json', 'r') as f:
        SAMPLE_SYSTEMS_DATA =  json.loads(f.read())

    def test_add_system(self):
        systems = Systems()

        for system_data in self.SAMPLE_SYSTEMS_DATA:
            systems.add_system(system_data)

        # NOTE: The number of stars in a certain region should be constant.
        # NOTE: There are 146 stars within 20 lightyears of star system 'Warkawa'
        self.assertEquals(len(systems.list), 146)

    def test_iter(self):
        systems = Systems()
        for system_data in self.SAMPLE_SYSTEMS_DATA:
            systems.add_system(system_data)

        for item in systems:
            pass
    
    def test_get(self):
        systems = Systems()
        for system_data in self.SAMPLE_SYSTEMS_DATA:
            systems.add_system(system_data)

        s = systems.get('Warkawa')

        self.assertIs(type(s), System)
        self.assertEquals(s.name, 'Warkawa')

    def test_remove(self):
        systems = Systems()
        for system_data in self.SAMPLE_SYSTEMS_DATA:
            systems.add_system(system_data)

        self.assertIs(type(systems.get('Col 285 Sector FG-D a42-3')), System)

        systems.remove('Col 285 Sector FG-D a42-3')

        self.assertIs(systems.get('Col 285 Sector FG-D a42-3'), None)


