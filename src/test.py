import unittest
from src.domain import functions


class TestCase(unittest.TestCase):
    def test_sum(self):
        r = functions.sum(20, 30)
        self.assertEqual(r, 50)  # add assertion here

    def test_nosum(self):
        r = functions.sum(20, 40)
        self.assertEqual(r, 90)

if __name__ == '__main__':
    unittest.main()
