import unittest
from ..web import *

class TestUrl(unittest.TestCase):


    def test_create_url(self):
        a = {'I': ['fuck', 'you'], 'path': 1}
        b = ('I', 'I')
        r = create_url('http://', b, path='/api/', params=a)
        self.assertEqual(r, 'http:///api/?I=I&I=fuck&I=you&path=1')