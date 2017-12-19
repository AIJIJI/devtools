from unittest import TestCase, main 
from devtools.linux import lxrun
from devtools import strtodict


class MainTestCase(TestCase):
    
    def test_strtodict(self):
        text = 'k1, v1\nk2 ,v2'
        res = strtodict(text, 'c', ',')
        d = {'k1':'v1', 'k2':'v2'}
        self.assertEqual(res, d)

        text = '''k1, d1v1, d2v1
                  k2, d1v2, d2v2, d3v2,
                  k3, d1v3, d2v3
                '''
        res = strtodict(text, 'cs', ',', ',')
        self.assertEqual(res, [{'k1': 'd1v1', 'k2': 'd1v2', 'k3':'d1v3'}, {'k1': 'd2v1','k2':'d2v2', 'k3':'d2v3'},{'k2':'d3v2'}])

        text = 'k1 k2\nv1 v2 v3\n'
        res = strtodict(text, 'r', ' ')
        self.assertEqual(res, d)

main()        
