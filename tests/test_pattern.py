__author__ = "Lukas Mahler"
__version__ = "1.0.0"
__date__ = "04.12.2024"
__email__ = "m@hler.eu"
__status__ = "Production"


import unittest

from cs2pattern import check_rare

inputs = [
    [(False, None), ("★ Bayonet | Gamma Doppler (Factory New)", 334)],
    [(False, None), ("	★ Broken Fang Gloves | Jade (Factory New)", 7)],
    [(True, ("gem_purple", 5)), ("Desert Eagle | Heat Treated (Field-Tested)", 29)],
    [(False, None), ("Desert Eagle | Heat Treated (Field-Tested)", 122)],
    [(True, ("gem_blue", 1)), ("Desert Eagle | Heat Treated (Field-Tested)", 490)],
    [(False, None), ("AWP |  Asiimov (Field-Tested)", 33)],
]


class TestPattern(unittest.TestCase):

    def test_pattern(self):

        for expected, args in inputs:
            with self.subTest(args=args):
                self.assertEqual(check_rare(*args), expected)


if __name__ == '__main__':
    unittest.main()
