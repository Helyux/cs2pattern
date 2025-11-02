__author__ = "Lukas Mahler"
__version__ = "1.0.0"
__date__ = "02.11.2025"
__email__ = "m@hler.eu"
__status__ = "Production"


import unittest

from cs2pattern import (
    abyss,
    berries,
    blaze,
    check_rare,
    fade,
    fire_and_ice,
    gem_black,
    gem_blue,
    gem_diamond,
    gem_gold,
    gem_green,
    gem_pink,
    gem_purple,
    gem_white,
    get_pattern_dict,
    grinder,
    hive_blue,
    hive_orange,
    moonrise,
    nocts,
    paw,
    phoenix,
    pussy,
    PatternInfo,
)
from cs2pattern.check import ICON_MAP, _normalize_input

inputs = [

    # Test Random
    [(False, None, None), ("★ Bayonet | Gamma Doppler (Factory New)", 3344)],
    [(False, None, None), ("	★ Broken Fang Gloves | | Jade (Factory New)", 7)],
    [(False, None, None), ("Desert Eagle | Heat Treated (Field-Tested)", 122)],
    [(False, None, None), ("AWP |  Asiimov (Field-Tested)", 33)],

    # Test Abyss
    [(True, 'white_scope', None), ("SSG 08 | Abyss (Field-Tested)", 148)],
    [(False, None, None), ("SSG 08 | Abyss (Field-Tested)", 152)],
    [(False, None, None), ("AWP | Abyss (Fielt-dested)", 148)],

    # Test berries
    [(True, 'gem_blue', None), ("Five-SeveN | Berries And Cherries (Factory New)", 80)],
    [(True, 'gem_red', None), ("Five-SeveN | Berries And Cherries (Factory New)", 182)],
    [(False, None, None), ("Five-SeveN | Berries And Cherries (Factory New)", 82)],

    # Test blaze
    [(True, 'blaze', None), ("★ Karambit | Case Hardened (Field-Tested)", 896)],
    [(True, 'blaze', None), ("★ Karambit | Case Hardened (Field-Tested)", 941)],
    [(False, None, None), ("★ Karambit | Case Hardened (Field-Tested)", 878)],
    [(False, None, None), ("★ Flip Knife | Case Hardened (Field-Tested)", 896)],

    # Test fire & ice
    [(True, 'fire_and_ice', None), ("★ Bayonet | Marble Fade (Factory New)", 16)],
    [(False, None, None), ("★ Bayonet | Marble Fade (Factory New)", 55)],
    [(True, 'fire_and_ice', None), ("★ Flip Knife | Marble Fade (Factory New)", 16)],
    [(False, None, None), ("★ Flip Knife | Marble Fade (Factory New)", 55)],
    [(True, 'fire_and_ice', None), ("★ Gut Knife | Marble Fade (Factory New)", 16)],
    [(False, None, None), ("★ Gut Knife | Marble Fade (Factory New)", 55)],
    [(True, 'fire_and_ice', None), ("★ Karambit | Marble Fade (Factory New)", 701)],
    [(True, 'fire_and_ice', None), ("★ Karambit | Marble Fade (Factory New)", 541)],
    [(True, 'fire_and_ice', None), ("★ Karambit | Marble Fade (Factory New)", 16)],
    [(False, None, None), ("★ Karambit | Marble Fade (Factory New)", 55)],
    [(False, None, None), ("★ Karambit | Marble Fade (Factory New)", 999)],

    # Test fade
    [(True, 'fade', (1, 10)), ("★ Karambit | Fade (Factory New)", 412)],
    [(True, 'fade', (10, 10)), ("★ Karambit | Fade (Factory New)", 541)],
    [(True, 'fade', (1, 10)), ("★ M9 Bayonet | Fade (Factory New)", 763)],
    [(True, 'fade', (10, 10)), ("★ M9 Bayonet | Fade (Factory New)", 326)],
    [(True, 'fade', (1, 10)), ("★ Talon Knife | Fade (Factory New)", 412)],
    [(True, 'fade', (10, 10)), ("★ Talon Knife | Fade (Factory New)", 541)],
    [(True, 'fade', (1, 10)), ("AWP | Fade (Factory New)", 412)],
    [(True, 'fade', (10, 10)), ("AWP | Fade (Factory New)", 541)],
    [(True, 'fade', (1, 10)), ("M4A1-S | Fade (Factory New)", 374)],
    [(True, 'fade', (10, 10)), ("M4A1-S | Fade (Factory New)", 873)],
    [(False, None, None), ("★ Karambit | Fade (Factory New)", 999)],

    # Test gem blue
    [(True, 'gem_blue', (1, 14)), ("AK-47 | Case Hardened (Field-Tested)", 661)],
    [(True, 'gem_blue', (2, 6)), ("★ Bayonet | Case Hardened (Factory New)", 592)],
    [(True, 'gem_blue', (2, 4)), ("Desert Eagle | Heat Treated (Field-Tested)", 148)],
    [(True, 'gem_blue', (4, 10)), ("Five-SeveN | Case Hardened (Factory New)", 670)],
    [(True, 'gem_blue', (3, 6)), ("★ Flip Knife | Case Hardened (Factory New)", 151)],
    [(True, 'gem_blue', (5, 5)), ("MAC-10 | Case Hardened (Factory New)", 18)],
    [(False, None, None), ("★ Karambit | Case Hardened (Factory New)", 123)],

    # Test gem diamond
    [(True, 'gem_diamond', (4, 7)), ("★ Karambit | Gamma Doppler (Factory New)", 717)],
    [(False, None, None), ("★ Karambit | Gamma Doppler (Factory New)", 555)],

    # Test gem gold
    [(True, 'gem_gold', None), ("AK-47 | Case Hardened (Field-Tested)", 219)],
    [(True, 'gem_gold', None), ("★ Bayonet | Case Hardened (Factory New)", 395)],
    [(True, 'gem_gold', None), ("★ Karambit | Case Hardened (Factory New)", 231)],
    [(False, None, None), ("Five-SeveN | Case Hardened (Factory New)", 500)],

    # Test gem green
    [(True, 'gem_green', (2, 3)), ("SSG 08 | Acid Fade (Factory New)", 575)],
    [(False, None, None), ("SSG 08 | Acid Fade (Factory New)", 123)],

    # Test gem pink
    [(True, 'gem_pink', None), ("Glock-18 | Pink DDPAT (Factory New)", 600)],
    [(False, None, None), ("Glock-18 | Pink DDPAT (Factory New)", 700)],

    # Test gem purple
    [(True, 'gem_purple', (2, 7)), ("Desert Eagle | Heat Treated (Factory New)", 599)],
    [(False, None, None), ("Desert Eagle | Heat Treated (Factory New)", 999)],
    [(True, 'gem_purple', (1, 6)), ("Tec-9 | Sandstorm (Factory New)", 328)],
    [(True, 'gem_purple', (2, 6)), ("Tec-9 | Sandstorm (Factory New)", 862)],
    [(True, 'gem_purple', (3, 6)), ("Tec-9 | Sandstorm (Factory New)", 70)],
    [(True, 'gem_purple', (4, 6)), ("Tec-9 | Sandstorm (Factory New)", 552)],
    [(True, 'gem_purple', (5, 6)), ("Tec-9 | Sandstorm (Factory New)", 83)],
    [(True, 'gem_purple', (6, 6)), ("Tec-9 | Sandstorm (Factory New)", 583)],
    [(False, None, None), ("Tec-9 | Sandstorm (Factory New)", 123)],

    # Test gem white
    [(True, 'gem_white', None), ("★ Skeleton Knife | Urban Masked (Factory New)", 299)],
    [(False, None, None), ("★ Skeleton Knife | Urban Masked (Factory New)", 403)],

    # Test grinder
    [(True, 'gem_black', (1, 4)), ("Glock-18 | Grinder (Factory New)", 384)],
    [(False, None, None), ("Glock-18 | Grinder (Factory New)", 123)],

    # Test hive
    [(True, 'blue_hive', (5, 6)), ("AWP | Electric Hive (Factory New)", 853)],
    [(True, 'orange_hive', (6, 6)), ("AWP | Electric Hive (Factory New)", 42)],
    [(False, None, None), ("AWP | Electric Hive (Factory New)", 500)],

    # Test moonrise
    [(True, 'star', (3, 12)), ("Glock-18 | Moonrise (Factory New)", 66)],
    [(False, None, None), ("Glock-18 | Moonrise (Factory New)", 555)],

    # Test nocts
    [(True, 'gem_black', None), ("★ Sport Gloves | Nocts (Field-Tested)", 231)],
    [(False, None, None), ("★ Sport Gloves | Nocts (Field-Tested)", 123)],

    # Test paw
    [(True, 'golden_cat', None), ("AWP | Paw (Factory New)", 350)],
    [(False, None, None), ("AWP | Paw (Factory New)", 999)],

    # Test phoenix
    [(True, 'phoenix', (3, 7)), ("Galil AR | Phoenix Blacklight (Factory New)", 619)],
    [(False, None, None), ("Galil AR | Phoenix Blacklight (Factory New)", 777)],

    # Test pussy
    [(True, 'pussy', None), ("Five-SeveN | Kami (Factory New)", 590)],
    [(False, None, None), ("Five-SeveN | Kami (Factory New)", 300)],
]


class TestPattern(unittest.TestCase):

    def test_pattern(self):

        for expected, args in inputs:
            with self.subTest(args=args):
                normalized = _normalize_input(*args)
                if normalized:
                    weapon, skin, normalized_pattern = normalized
                else:
                    weapon = skin = normalized_pattern = None
                ordered = expected[2] is not None
                structured_expected = PatternInfo(
                    weapon=weapon,
                    skin=skin,
                    pattern=normalized_pattern,
                    rare=expected[0],
                    name=expected[1],
                    ordered=ordered,
                    order=expected[2],
                    icon=ICON_MAP.get(expected[1]) if expected[1] else None,
                )
                self.assertEqual(check_rare(*args), structured_expected)

    def test_group_icons_defined(self):
        groups = set()
        for weapon_groups in get_pattern_dict().values():
            for group_list in weapon_groups.values():
                for group in group_list:
                    groups.add(group.get('name'))

        missing = {name for name in groups if name and name not in ICON_MAP}
        self.assertFalse(missing, f"Missing icons for groups: {sorted(missing)}")


class TestModularHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patterns = get_pattern_dict()

    def _expect_group(self, skin: str, weapon: str, group_name: str) -> tuple[list[int], bool]:
        weapon_groups = self.patterns.get(skin, {}).get(weapon, [])
        for group in weapon_groups:
            if group.get('name') == group_name:
                return list(group.get('pattern', [])), bool(group.get('ordered', False))
        self.fail(f"Group '{group_name}' not found for skin '{skin}' and weapon '{weapon}'")

    def test_simple_helpers(self):
        cases = [
            (abyss, 'abyss', 'ssg 08', 'white_scope'),
            (blaze, 'case hardened', 'karambit', 'blaze'),
            (gem_diamond, 'gamma doppler', 'karambit', 'gem_diamond'),
            (gem_green, 'acid fade', 'ssg 08', 'gem_green'),
            (gem_pink, 'pink ddpat', 'glock-18', 'gem_pink'),
            (grinder, 'grinder', 'glock-18', 'gem_black'),
            (hive_blue, 'electric hive', 'awp', 'blue_hive'),
            (hive_orange, 'electric hive', 'awp', 'orange_hive'),
            (moonrise, 'moonrise', 'glock-18', 'star'),
            (nocts, 'nocts', 'sport gloves', 'gem_black'),
            (phoenix, 'phoenix blacklight', 'galil ar', 'phoenix'),
            (pussy, 'kami', 'five-seven', 'pussy'),
        ]

        for func, skin, weapon, group_name in cases:
            with self.subTest(func=func.__name__):
                expected = self._expect_group(skin, weapon, group_name)
                self.assertEqual(func(), expected)

    def test_berries_helper(self):
        gem_red_group, _ = self._expect_group('berries and cherries', 'five-seven', 'gem_red')
        gem_blue_group, _ = self._expect_group('berries and cherries', 'five-seven', 'gem_blue')
        patterns, ordered = berries()
        self.assertEqual(patterns, gem_red_group + gem_blue_group)
        self.assertFalse(ordered)

    def test_paw_helper(self):
        golden, _ = self._expect_group('paw', 'awp', 'golden_cat')
        stoner, _ = self._expect_group('paw', 'awp', 'stoner_cat')
        patterns, ordered = paw()
        self.assertEqual(patterns, golden + stoner)
        self.assertFalse(ordered)

    def test_fire_and_ice_helper(self):
        for weapon in ['bayonet', 'flip knife', 'gut knife', 'karambit']:
            with self.subTest(weapon=weapon):
                expected = self._expect_group('marble fade', weapon, 'fire_and_ice')
                self.assertEqual(fire_and_ice(weapon), expected)

    def test_fire_and_ice_unsupported_weapon(self):
        self.assertIsNone(fire_and_ice('m9 bayonet'))

    def test_fade_helper(self):
        weapons = [
            'awp',
            'karambit',
            'm9 bayonet',
            'm4a1-s',
            'talon knife',
        ]

        for weapon in weapons:
            with self.subTest(weapon=weapon):
                expected = self._expect_group('fade', weapon, 'fade')
                self.assertEqual(fade(weapon), expected)

        self.assertIsNone(fade('butterfly knife'))

    def test_gem_black_helper(self):
        weapons = [
            'classic knife',
            'flip knife',
            'nomad knife',
            'paracord knife',
            'shadow daggers',
            'skeleton knife',
            'stiletto knife',
            'ursus knife',
        ]

        for weapon in weapons:
            with self.subTest(weapon=weapon):
                expected = self._expect_group('scorched', weapon, 'gem_black')
                self.assertEqual(gem_black(weapon), expected)

        self.assertIsNone(gem_black('unsupported'))

    def test_gem_blue_helper(self):
        cases = {
            'ak-47': 'case hardened',
            'bayonet': 'case hardened',
            'bowie knife': 'case hardened',
            'butterfly knife': 'case hardened',
            'classic knife': 'case hardened',
            'desert eagle': 'heat treated',
            'falchion knife': 'case hardened',
            'five-seven': 'case hardened',
            'flip knife': 'case hardened',
            'gut knife': 'case hardened',
            'huntsman knife': 'case hardened',
            'hydra gloves': 'case hardened',
            'karambit': 'case hardened',
            'm9 bayonet': 'case hardened',
            'mac-10': 'case hardened',
            'navaja knife': 'case hardened',
            'nomad knife': 'case hardened',
            'paracord knife': 'case hardened',
            'shadow daggers': 'case hardened',
            'skeleton knife': 'case hardened',
            'stiletto knife': 'case hardened',
            'survival knife': 'case hardened',
            'talon knife': 'case hardened',
            'ursus knife': 'case hardened',
        }

        for weapon, skin in cases.items():
            with self.subTest(weapon=weapon):
                expected = self._expect_group(skin, weapon, 'gem_blue')
                self.assertEqual(gem_blue(weapon), expected)

        self.assertIsNone(gem_blue('unsupported'))

    def test_gem_gold_helper(self):
        cases = {
            'ak-47': 'case hardened',
            'bayonet': 'case hardened',
            'five-seven': 'case hardened',
            'karambit': 'case hardened',
        }

        for weapon, skin in cases.items():
            with self.subTest(weapon=weapon):
                expected = self._expect_group(skin, weapon, 'gem_gold')
                self.assertEqual(gem_gold(weapon), expected)

        self.assertIsNone(gem_gold('m4a1-s'))

    def test_gem_purple_helper(self):
        cases = {
            'desert eagle': 'heat treated',
            'galil ar': 'sandstorm',
            'tec-9': 'sandstorm',
        }

        for weapon, skin in cases.items():
            with self.subTest(weapon=weapon):
                expected = self._expect_group(skin, weapon, 'gem_purple')
                self.assertEqual(gem_purple(weapon), expected)

        self.assertIsNone(gem_purple('ak-47'))

    def test_gem_white_helper(self):
        cases = {
            'stiletto knife': 'urban masked',
            'skeleton knife': 'urban masked',
            'classic knife': 'urban masked',
            'flip knife': 'urban masked',
            'm9 bayonet': 'urban masked',
        }

        for weapon, skin in cases.items():
            with self.subTest(weapon=weapon):
                expected = self._expect_group(skin, weapon, 'gem_white')
                self.assertEqual(gem_white(weapon), expected)

        self.assertIsNone(gem_white('karambit'))


if __name__ == '__main__':
    unittest.main()
