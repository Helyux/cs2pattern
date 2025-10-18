__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "15.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


from typing import Optional, Sequence

from cs2pattern.check import get_pattern_dict

SPECIAL_PATTERN = get_pattern_dict()


def _lookup_group(skin: str, weapon: str, group_name: str) -> tuple[list[int], bool]:
    """
    Retrieve pattern data for a single group from the shared pattern dictionary.

    :param skin: Skin identifier (lower-case, matching the JSON keys).
    :type skin: str
    :param weapon: Weapon identifier (lower-case, matching the JSON keys).
    :type weapon: str
    :param group_name: Name of the group within the skin/weapon entry.
    :type group_name: str

    :return: A tuple containing the list of pattern ids and the ordered flag.
    :rtype: tuple[list[int], bool]
    """

    groups = SPECIAL_PATTERN.get(skin, {}).get(weapon, [])
    for group in groups:
        if group.get('name') == group_name:
            return list(group.get('pattern', [])), bool(group.get('ordered', False))
    return [], False


def _lookup_first_group(
    weapon: str,
    group_name: str,
    skins: Sequence[str],
    default_ordered: bool,
) -> tuple[list[int], bool]:
    """
    Try to resolve a group across multiple skins for a given weapon.

    :param weapon: Weapon identifier.
    :type weapon: str
    :param group_name: Group to retrieve.
    :type group_name: str
    :param skins: Skins to inspect in order until the group is found.
    :type skins: Sequence[str]
    :param default_ordered: Ordered flag to fall back to if no data is found.
    :type default_ordered: bool

    :return: The first matching pattern list and ordered flag, or defaults.
    :rtype: tuple[list[int], bool]
    """

    weapon = weapon.lower()
    for skin in skins:
        patterns, ordered = _lookup_group(skin, weapon, group_name)
        if patterns:
            return patterns, ordered
    return [], default_ordered


def abyss() -> tuple[list[int], bool]:
    """
    Return a pattern list for white scoped 'SSG 08 | Abyss' skins.
    WARN: BS=White, FN=Light-Blue!

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('abyss', 'ssg 08', 'white_scope')


def berries() -> tuple[list[int], bool]:
    """
    Return gem red (182) or gem blue (80) 'Five-SeveN | Berries and Cherries' pattern list.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    red, _ = _lookup_group('berries and cherries', 'five-seven', 'gem_red')
    blue, _ = _lookup_group('berries and cherries', 'five-seven', 'gem_blue')
    return red + blue, False


def blaze() -> tuple[list[int], bool]:
    """
    Return a pattern list for blaze pattern '★ Karambit | Case Hardened'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('case hardened', 'karambit', 'blaze')


def fire_and_ice(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return a pattern list for 1st and 2nd max fire & ice pattern 'Marble Fade' skins.
    WARNING: This is only available for Bayonet, Flip Knife, Gut Knife & Karambit!

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_normalized = weapon.lower()
    weapon_options = {'bayonet', 'flip knife', 'gut knife', 'karambit'}

    if weapon_normalized in weapon_options:
        return _lookup_group('marble fade', weapon_normalized, 'fire_and_ice')
    else:
        return [], False


def gem_blue(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return a pattern list for bluegem 'Case Hardened' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    skin_options = {
        'ak-47': ('case hardened',),
        'bayonet': ('case hardened',),
        'desert eagle': ('heat treated',),
        'five-seven': ('case hardened',),
        'flip knife': ('case hardened',),
        'karambit': ('case hardened',),
    }

    weapon_normalized = weapon.lower()
    skins = skin_options.get(weapon_normalized)
    if not skins:
        return [], True
    return _lookup_first_group(weapon_normalized, 'gem_blue', skins, True)


def gem_diamond() -> tuple[list[int], bool]:
    """
    Return a pattern list for diamondgem 'Karambit | Gamma Doppler'.
    WARN: YOU HAVE TO VERIFY, THIS IS ONLY P1 GAMMA DOPPLERS!

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('gamma doppler', 'karambit', 'gem_diamond')


def gem_gold(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return a pattern list for goldgem 'Case Hardened' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    skin_options = {
        'ak-47': ('case hardened',),
        'bayonet': ('case hardened',),
        'five-seven': ('case hardened',),
        'karambit': ('case hardened',),
    }

    weapon_normalized = weapon.lower()
    skins = skin_options.get(weapon_normalized)
    if not skins:
        return [], False
    return _lookup_first_group(weapon_normalized, 'gem_gold', skins, False)


def gem_green() -> tuple[list[int], bool]:
    """
    Return a pattern list for max green 'SSG 08 | Acid Fade'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('acid fade', 'ssg 08', 'gem_green')


def gem_pink() -> tuple[list[int], bool]:
    """
    Return a pattern list for max pink 'Glock-18 | Pink DDPAT'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('pink ddpat', 'glock-18', 'gem_pink')


def gem_purple(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return a pattern list for purplegem 'Sandstorm' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    skin_options = {
        'desert eagle': ('heat treated',),
        'galil ar': ('sandstorm',),
        'tec-9': ('sandstorm',),
    }

    weapon_normalized = weapon.lower()
    skins = skin_options.get(weapon_normalized)
    if not skins:
        return [], True
    return _lookup_first_group(weapon_normalized, 'gem_purple', skins, True)


def gem_white(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return a pattern list for whitegem 'Urban Masked' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    skin_options = {
        'stiletto knife': ('urban masked',),
        'skeleton knife': ('urban masked',),
        'classic knife': ('urban masked',),
        'flip knife': ('urban masked',),
        'm9 bayonet': ('urban masked',),
    }

    weapon_normalized = weapon.lower()
    skins = skin_options.get(weapon_normalized)
    if not skins:
        return [], False
    return _lookup_first_group(weapon_normalized, 'gem_white', skins, False)


def grinder() -> tuple[list[int], bool]:
    """
    Return a pattern list for gem black 'Glock-18 | Grinder'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('grinder', 'glock-18', 'gem_black')


def hive_blue() -> tuple[list[int], bool]:
    """
    Return a pattern list for max blue 'AWP | Electric Hive'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('electric hive', 'awp', 'blue_hive')


def hive_orange() -> tuple[list[int], bool]:
    """
    Return a pattern list for max orange 'AWP | Electric Hive'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('electric hive', 'awp', 'orange_hive')


def moonrise() -> tuple[list[int], bool]:
    """
    Return a pattern list for star pattern 'Glock-18 | Moonrise'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('moonrise', 'glock-18', 'star')


def nocts() -> tuple[list[int], bool]:
    """
    Return a pattern list for gem black '★ Sport Gloves | Nocts'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('nocts', 'sport gloves', 'gem_black')


def paw() -> tuple[list[int], bool]:
    """
    Return a pattern list for golden cat and stoner cat pattern 'AWP | PAW'.

    Golden Cat: [41, 350] // Stoner Cat: [420]

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    golden, _ = _lookup_group('paw', 'awp', 'golden_cat')
    stoner, _ = _lookup_group('paw', 'awp', 'stoner_cat')
    return golden + stoner, False


def phoenix() -> tuple[list[int], bool]:
    """
    Return a pattern list for best pos visible phoenix 'Galil AR | Phoenix Blacklight'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('phoenix blacklight', 'galil ar', 'phoenix')


def pussy() -> tuple[list[int], bool]:
    """
    Return pattern list for pussy pattern 'Five-SeveN | Kami'.

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return _lookup_group('kami', 'five-seven', 'pussy')


def gem_black(weapon: str) -> tuple[list[int], bool]:
    """
    Return a pattern list for blackgem 'Scorched' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of patterns that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_normalized = weapon.lower()
    weapon_options = {
        'skeleton knife': ('scorched',),
        'stiletto knife': ('scorched',),
        'classic knife': ('scorched',),
        'ursus knife': ('scorched',),
        'paracord knife': ('scorched',),
        'nomad knife': ('scorched',),
        'shadow daggers': ('scorched',),
        'flip knife': ('scorched',),
    }

    skins = weapon_options.get(weapon_normalized)
    if not skins:
        return [], True
    return _lookup_first_group(weapon_normalized, 'gem_black', skins, True)


if __name__ == '__main__':
    exit(1)
