import unittest

from models import Traffic

# TODO : Test update funcs (make sure objs are empty before update, + properly populated after update)

class TrafficTest(unittest.TestCase):
    def test_Traffic_Sol(self):
        t = Traffic('Sol')
        self.assertIs(type(t.breakdown), dict)
