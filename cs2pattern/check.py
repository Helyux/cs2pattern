__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "03.12.2024"
__email__ = "m@hler.eu"
__status__ = "Development"


import json
import os
import re
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "pattern.json")
with open(json_path, "r") as file:
    SPECIAL_PATTERN = json.load(file)


def _normalize_input(market_hash: str, pattern: int, floatvalue: Optional[float] = None) -> Optional[tuple[str, str, int, Optional[float]]]:
    """
    Normalize and validate CS2 item input.

    :param market_hash: The market hash of the item.
    :type market_hash: str

    :param pattern: The pattern, which should be numeric and between 0-1000 (inclusive).
    :type pattern: int
    :param floatvalue: The float value, which must be a float between 0 and 1 (exclusive).
    :type floatvalue: Optional[float]

    :return: A tuple of the normalized weapon, skin, pattern, and floatvalue or None if we failed normalizing.
    :rtype: Optional[tuple[str, str, int, Optional[float]]]

    :raises ValueError: If any input validation fails.
    """

    # Normalize market_hash
    market_hash = re.sub(r"\s+", " ", market_hash.replace("★ ", "").lower()).strip()

    # Extract weapon and skin
    if " | " not in market_hash:
        return

    weapon, skin = market_hash.split(" | ", 1)
    skin = re.sub(r"\s*\(.*?\)$", "", skin).strip()

    # Validate pattern
    if not (0 <= pattern <= 1000):
        return

    # Validate floatvalue
    if floatvalue is not None and not (0 < floatvalue < 1):
        return

    return weapon, skin, pattern, floatvalue


def _check_special(normalized_data: tuple[str, str, int, Optional[float]]) -> Optional[tuple[str, int]]:
    weapon, skin, pattern, floatvalue = normalized_data

    # Check if skin and weapon exist in the pattern data
    if skin not in SPECIAL_PATTERN or weapon not in SPECIAL_PATTERN[skin]:
        return None

    weapon_data = SPECIAL_PATTERN[skin][weapon]

    # If weapon_data is a list (multiple pattern groups)
    if isinstance(weapon_data, list):
        for group in weapon_data:
            if pattern in group['pattern']:
                index = group['pattern'].index(pattern) if group['ordered'] else -1
                return group['name'], index+1

    # If weapon_data is a single group (dict)
    elif isinstance(weapon_data, dict):
        if pattern in weapon_data.get('pattern', []):
            index = weapon_data['pattern'].index(pattern) if weapon_data['ordered'] else -1
            return weapon_data['name'], index+1


    # If a float value is provided and the special provides min check that
    if floatvalue:
        if 'float_min' in weapon_data:
            if floatvalue > weapon_data['float_min']:
                return weapon_data['name'], -1

    return None

def check_rare(market_hash: str, pattern: int, floatvalue: Optional[float] = None) -> tuple[bool, Optional[tuple[str, int]]]:

    normalized = _normalize_input(market_hash, pattern, floatvalue)
    if not normalized:
        return False, None

    special = _check_special(normalized)
    if special:
        return True, special

    return False, None



def abyss(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'SSG 08 | Abyss' patterned skin.

    White scope patterns: [54, 148, 167, 208, 669, 806, 911, 985]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["ssg 08", "abyss"]
    special_pattern = [54, 148, 167, 208, 669, 806, 911, 985]
    return False


def berries_and_cherries(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Five-SeveN | Berries and Cherries' patterned skin.

    max red pattern: 182 / max blue pattern: 80

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["five-seven", "berries and cherries"]
    special_pattern = [182, 80]
    return False


def blackiimov(market_hash: str, floatvalue: float) -> bool:
    """
    Determines if a skin qualifies as a blackiimov based on its market hash and floatvalue.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param floatvalue: The float value of the item.
    :type floatvalue: float

    :return: A boolean indicating whether the skin is a blackiimov.
    :rtype: bool
    """

    keywords = ["awp", "asiimov"]
    return False


def blaze(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special blaze patterned case hardened skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    weapon_options = [
        [["ak-47", "case hardened"], [784, 219]],
        [["karambit", "case hardened"], [819, 896, 939, 941]],
    ]

    return False


def fire_and_ice(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a 1st or 2nd max fire & ice marble fade pattern.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    weapon_options = [
        [["bayonet", "marble fade"], [412, 16, 146, 241, 359, 393, 541, 602, 649, 688, 701]],
        [["karambit", "marble fade"], [412, 16, 146, 241, 359, 393, 541, 602, 649, 688, 701]],
    ]

    return False


def gem_blue(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special bluegem patterned case hardened skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    weapon_options = [
        [["ak-47", "case hardened"], [661, 670, 955, 179, 387, 151, 321, 592, 809, 555, 828, 760, 168, 617], True],
        [["five-seven", "case hardened"], [278, 690, 868, 670, 363, 872, 648, 532, 689, 321]],
        [["flip knife", "case hardened"], [670, 321, 151, 592, 661, 555]],
        [["karambit", "case hardened"], [387, 888, 442, 853, 269, 470, 905, 809, 902, 776, 463, 73, 510]],
        [["desert eagle", "heat treated"], [490, 148, 69, 704]]
    ]

    return False


def gem_diamond(market_hash: str, pattern: int, p1: bool = False) -> bool:
    """
    Determines if an item is a special 'Karambit | Gamma Doppler' diamond gem.
    YOU HAVE TO VERIFY ITS ONLY P1 DOPPLERS!!!

    Most Blue (in order!): [547, 630, 311, 717, 445, 253, 746]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int
    :param p1: Verify you provided a Phase 1 Gamma Doppler, defaults to False.
    :type: p1: bool

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    if not p1:
        return False

    keywords = ["karambit", "gamma doppler"]
    special_pattern = [547, 630, 311, 717, 445, 253, 746]
    return False


def gem_gold(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special gold gem patterned case hardened skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    weapon_options = [
        [["ak-47", "case hardened"], [784, 219]],
        [["five-seven", "case hardened"], [691]],
        [["karambit", "case hardened"], [896, 231, 939, 388]],
    ]

    return False


def gem_green(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'SSG 08 | Acid Fade' patterned skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["ssg 08", "acid fade"]
    special_pattern = [576, 575, 449]
    return False


def gem_pink(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Glock-18 | Pink DDPAT' patterned skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["glock-18", "pink ddpat"]
    special_pattern = [568, 600]
    return False


def gem_purple(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special purple gem patterned sandstorm skin.

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    weapon_options = [
        [["galil ar", "sandstorm"], [583, 761, 739, 178]],
        [["tec-9", "sandstorm"], [70, 328, 862, 583, 552]],
        [["desert eagle", "heat treated"], [172, 599, 156, 293, 29, 944, 133]]
    ]

    return False


def grinder(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Glock-18 | Grinder' patterned skin.

    Black (in order!): [384, 916, 811, 907]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["glock-18", "grinder"]
    special_pattern = [384, 916, 811, 907]
    return False


def hive(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'AWP | Electric Hive' patterned skin.

    Blue Hive (in order!): [273, 436, 902, 23, 853, 262]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["awp", "electric hive"]
    special_pattern = [273, 436, 902, 23, 853, 262]
    return False


def moonrise(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Glock-18 | Moonrise' patterned skin.

    Best pattern: [58, 59, 66, 90, 102, 224, 601, 628, 694, 706, 837, 864]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["glock-18", "moonrise"]
    special_pattern = [58, 59, 66, 90, 102, 224, 601, 628, 694, 706, 837, 864]
    return False


def paw(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'AWP | PAW' patterned skin.

    Golden Cat: [41, 350]
    Stoner Cat: [420]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["awp", "paw"]
    special_pattern = [41, 350, 420]
    return False


def phoenix(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Galil AR | Phoenix Blacklight' patterned skin.

    Best pattern (in order!): [755, 963, 619, 978, 432, 289, 729]

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["galil ar", "phoenix blacklight"]
    special_pattern = [755, 963, 619, 978, 432, 289, 729]
    return False


def pussy(market_hash: str, pattern: int) -> bool:
    """
    Determines if an item is a special 'Five-SeveN | Kami' patterned skin.

    Pussy pattern: [590, 909] / 909 is ohnepixels pattern of choice

    :param market_hash: Name/Market hash of the item.
    :type market_hash: str
    :param pattern: Pattern index of the skin.
    :type pattern: int

    :return: Whether the skin matches the specified name and special pattern.
    :rtype: bool
    """

    keywords = ["five-seven", "kami"]
    special_pattern = [590, 909]
    return False


def webs():
        return False

if __name__ == '__main__':
    exit(1)
