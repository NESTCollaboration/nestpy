import unittest
from nestpy import nestpy

class NESTcalcTestt(unittest.TestCase):
    def test_construct(self):
        nestpy.NESTcalc()

    def test_binomial_fluct(self):
        x = nestpy.NESTcalc()
        y = nestpy.NESTcalc().BinomFluct(100, 0.3)
        print(y)

if __name__ == '__main__':
    unittest.main()
