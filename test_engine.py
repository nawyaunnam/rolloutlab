import unittest
from engine import Flag, decide, experiment, bucket

class RolloutTests(unittest.TestCase):
    def test_monotonic_cohorts(self):
        small, large = Flag('x',1,10), Flag('x',2,40)
        for i in range(1000):
            if decide(small,str(i))['enabled']:
                self.assertTrue(decide(large,str(i))['enabled'])
    def test_override_precedence(self):
        f = Flag('x',1,100,allow=frozenset({'a'}),deny=frozenset({'a'}))
        self.assertEqual(decide(f,'a')['reason'], 'explicit-deny')
        self.assertFalse(decide(Flag('x',1,100,enabled=False),'a')['enabled'])
    def test_targeting(self):
        f = Flag('x',1,100,attributes={'plan':'pro'})
        self.assertFalse(decide(f,'a',{'plan':'free'})['enabled'])
        self.assertTrue(decide(f,'a',{'plan':'pro'})['enabled'])
    def test_stability_and_weight_order(self):
        for i in range(100):
            self.assertEqual(experiment('x',str(i),{'a':50,'b':50}), experiment('x',str(i),{'b':50,'a':50}))
        self.assertNotEqual(bucket('a:b','c'),bucket('a','b:c'))
    def test_invalid_and_boundaries(self):
        with self.assertRaises(ValueError): Flag('x',1,101)
        with self.assertRaises(ValueError): experiment('x','a',{'a':90})
        self.assertFalse(decide(Flag('x',1,0),'a')['enabled'])
        self.assertTrue(decide(Flag('x',1,100),'a')['enabled'])
    def test_cohort_distribution(self):
        enabled = sum(decide(Flag('x',1,25),str(i))['enabled'] for i in range(10000))
        self.assertTrue(2300 < enabled < 2700)
