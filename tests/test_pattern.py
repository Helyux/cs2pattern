__author__ = "Lukas Mahler"
__version__ = "1.0.0"
__date__ = "04.12.2024"
__email__ = "m@hler.eu"
__status__ = "Production"


import unittest

from cs2pattern import check_rare

inputs = [

    # Test Random
    [(False, None), ("★ Bayonet | Gamma Doppler (Factory New)", 3344)],
    [(False, None), ("	★ Broken Fang Gloves | | Jade (Factory New)", 7)],
    [(False, None), ("Desert Eagle | Heat Treated (Field-Tested)", 122)],
    [(False, None), ("AWP |  Asiimov (Field-Tested)", 33)],

    # Test Abyss
    [(True, ("white_scope", -1)), ("SSG 08 | Abyss (Field-Tested)", 148)],
    [(False, None), ("SSG 08 | Abyss (Field-Tested)", 152)],
    [(False, None), ("AWP | Abyss (Fielt-dested)", 1523)],

    # Test berries
    [(True, ("max_blue", -1)), ("Five-SeveN | Berries And Cherries (Factory New)", 80)],
    [(True, ("max_red", -1)), ("Five-SeveN | Berries And Cherries (Factory New)", 182)],
    [(False, None), ("Five-SeveN | Berries And Cherries (Factory New)", 82)],

    # Test blaze
    [(True, ("blaze", -1)), ("★ Karambit | Case Hardened (Field-Tested)", 896)],
    [(True, ("blaze", -1)), ("★ Karambit | Case Hardened (Field-Tested)", 941)],
    [(False, None), ("★ Karambit | Case Hardened (Field-Tested)", 878)],
    [(False, None), ("★ Flip Knife | Case Hardened (Field-Tested)", 896)],

    # Test fire & ice
    [(True, ("fire_and_ice", -1)), ("★ Bayonet | Marble Fade (Factory New)", 16)],
    [(False, None), ("★ Bayonet | Marble Fade (Factory New)", 55)],
    [(True, ("fire_and_ice", -1)), ("★ Flip Knife | Marble Fade (Factory New)", 16)],
    [(False, None), ("★ Flip Knife | Marble Fade (Factory New)", 55)],
    [(True, ("fire_and_ice", -1)), ("★ Gut Knife | Marble Fade (Factory New)", 16)],
    [(False, None), ("★ Gut Knife | Marble Fade (Factory New)", 55)],
    [(True, ("fire_and_ice", -1)), ("★ Karambit | Marble Fade (Factory New)", 701)],
    [(True, ("fire_and_ice", -1)), ("★ Karambit | Marble Fade (Factory New)", 541)],
    [(True, ("fire_and_ice", -1)), ("★ Karambit | Marble Fade (Factory New)", 16)],
    [(False, None), ("★ Karambit | Marble Fade (Factory New)", 55)],
    [(False, None), ("★ Karambit | Marble Fade (Factory New)", 999)],

    # Test gem blue
    [(True, ("gem_blue", 1)), ("AK-47 | Case Hardened (Field-Tested)", 661)],
    [(True, ("gem_blue", 4)), ("Five-SeveN | Case Hardened (Factory New)", 670)],
    [(True, ("gem_blue", 3)), ("★ Flip Knife | Case Hardened (Factory New)", 151)],
    [(False, None), ("★ Karambit | Case Hardened (Factory New)", 123)],

    # Test gem diamond
    [(True, ("gem_diamond", 4)), ("★ Karambit | Gamma Doppler (Factory New)", 717)],
    [(False, None), ("★ Karambit | Gamma Doppler (Factory New)", 555)],

    # Test gem gold
    [(True, ("gem_gold", -1)), ("AK-47 | Case Hardened (Field-Tested)", 219)],
    [(True, ("gem_gold", -1)), ("★ Karambit | Case Hardened (Factory New)", 231)],
    [(False, None), ("Five-SeveN | Case Hardened (Factory New)", 500)],

    # Test gem green
    [(True, ("gem_green", 2)), ("SSG 08 | Acid Fade (Factory New)", 575)],
    [(False, None), ("SSG 08 | Acid Fade (Factory New)", 123)],

    # Test gem pink
    [(True, ("gem_pink", -1)), ("Glock-18 | Pink DDPAT (Factory New)", 600)],
    [(False, None), ("Glock-18 | Pink DDPAT (Factory New)", 700)],

    # Test gem purple
    [(True, ("gem_purple", 2)), ("Desert Eagle | Heat Treated (Factory New)", 599)],
    [(False, None), ("Desert Eagle | Heat Treated (Factory New)", 999)],

    # Test grinder
    [(True, ("max_black", 1)), ("Glock-18 | Grinder (Factory New)", 384)],
    [(False, None), ("Glock-18 | Grinder (Factory New)", 123)],

    # Test hive
    [(True, ("blue_hive", 5)), ("AWP | Electric Hive (Factory New)", 853)],
    [(False, None), ("AWP | Electric Hive (Factory New)", 500)],

    # Test moonrise
    [(True, ("star", 3)), ("Glock-18 | Moonrise (Factory New)", 66)],
    [(False, None), ("Glock-18 | Moonrise (Factory New)", 555)],

    # Test paw
    [(True, ("golden_cat", -1)), ("AWP | Paw (Factory New)", 350)],
    [(False, None), ("AWP | Paw (Factory New)", 999)],

    # Test phoenix
    [(True, ("phoenix", 3)), ("Galil AR | Phoenix Blacklight (Factory New)", 619)],
    [(False, None), ("Galil AR | Phoenix Blacklight (Factory New)", 777)],

    # Test pussy
    [(True, ("pussy", -1)), ("Five-SeveN | Kami (Factory New)", 590)],
    [(False, None), ("Five-SeveN | Kami (Factory New)", 300)],
]


class TestPattern(unittest.TestCase):

    def test_pattern(self):

        for expected, args in inputs:
            with self.subTest(args=args):
                self.assertEqual(check_rare(*args), expected)


if __name__ == '__main__':
    unittest.main()
