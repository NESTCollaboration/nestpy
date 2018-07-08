import unittest
from nestpy import nestpy

class MainTest(unittest.TestCase):
    def test_add(self):
        # test that 1 + 1 = 2
        self.assertEqual(nestpy.add(1, 1), 2)

    def test_subtract(self):
        # test that 1 - 1 = 0
        self.assertEqual(nestpy.subtract(1, 1), 0)

if __name__ == '__main__':
    unittest.main()
