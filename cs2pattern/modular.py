__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "28.03.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


from typing import Optional


def abyss() -> tuple[list[int], bool]:
    """
    Return pattern list for white scoped 'SSG 08 | Abyss' skins.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [54, 148, 167, 208, 669, 806, 911, 985], False


def berries() -> tuple[list[int], bool]:
    """
    Return max red (182) or max blue (80) 'Five-SeveN | Berries and cherries' pattern list.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [182, 80], False


def blaze() -> tuple[list[int], bool]:
    """
    Return pattern list for blaze pattern '★ Karambit | Case Hardened'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [819, 896, 939, 941], False


def fire_and_ice(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return pattern list for 1st & 2nd max fire and ice pattern 'Marble Fade' skins.
    WARNING: This is only available for Bayonet, Flip Knife, Gut Knife & Karambit!

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_options = {'bayonet', 'flip knife', 'gut knife', 'karambit'}

    if weapon in weapon_options:
        return [412, 16, 146, 241, 359, 393, 541, 602, 649, 688, 701], False
    else:
        return [], False


def gem_blue(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return pattern list for bluegem 'Case Hardened' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_options = {
        'ak-47': [661, 670, 955, 179, 387, 151, 321, 592, 809, 555, 828, 760, 168, 617],
        'five-seven': [278, 690, 868, 670, 363, 872, 648, 532, 689, 321],
        'flip knife': [670, 321, 151, 592, 661, 555],
        'karambit': [387, 888, 442, 853, 269, 470, 905, 809, 902, 776, 463, 73, 510],
        'desert eagle': [490, 148, 69, 704],
    }

    return weapon_options.get(weapon, []), True


def gem_diamond() -> tuple[list[int], bool]:
    """
    Return pattern list for diamondgem 'Karambit | Gamma Doppler'.
    WARN: YOU HAVE TO VERIFY, THIS IS ONLY P1 GAMMA DOPPLERS!

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [547, 630, 311, 717, 445, 253, 746], True


def gem_gold(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return pattern list for goldgem 'Case Hardened' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_options = {
        'ak-47': [784, 219],
        'five-seven': [691],
        'karambit': [231, 388],
    }

    return weapon_options.get(weapon, []), False


def gem_green() -> tuple[list[int], bool]:
    """
    Return pattern list for max green 'SSG 08 | Acid Fade'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [576, 575, 449], True


def gem_pink() -> tuple[list[int], bool]:
    """
    Return pattern list for max pink 'Glock-18 | Pink DDPAT'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [568, 600], False


def gem_purple(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return pattern list for purplegem 'Sandstorm' or 'Heat Treated' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_options = {
        'galil ar': [583, 761, 739, 178],
        'tec-9': [70, 328, 862, 583, 552],
        'desert eagle': [172, 599, 156, 293, 29, 944, 133],
    }

    return weapon_options.get(weapon, []), True


def gem_white(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Return pattern list for whitegem 'Urban Masked' skins.

    :param weapon: The weapon for which to return the pattern list
    :type weapon: str

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: Optional[tuple[list[int], bool]]
    """

    weapon_options = {
        'stiletto knife': [402],
        'skeleton knife': [299],
        'classic knife': [402],
        'flip knife': [346],
        'm9 bayonet': [620],
    }

    return weapon_options.get(weapon, []), False


def grinder() -> tuple[list[int], bool]:
    """
    Return pattern list for max black 'Glock-18 | Grinder'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [384, 916, 811, 907], True


def hive() -> tuple[list[int], bool]:
    """
    Return pattern list for bluehive 'AWP | Electric Hive'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [273, 436, 902, 23, 853, 262], True


def moonrise() -> tuple[list[int], bool]:
    """
    Return pattern list for star pattern 'Glock-18 | Moonrise'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [58, 59, 66, 90, 102, 224, 601, 628, 694, 706, 837, 864], True


def paw() -> tuple[list[int], bool]:
    """
    Return pattern list for golden cat & stoner cat pattern 'AWP | PAW'.

    Golden Cat: [41, 350] // Stoner Cat: [420]

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [41, 350, 420], False


def phoenix() -> tuple[list[int], bool]:
    """
    Return pattern list for best pos visible phoenix 'Galil AR | Phoenix Blacklight'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [755, 963, 619, 978, 432, 289, 729], True


def pussy() -> tuple[list[int], bool]:
    """
    Return pattern list for pussy pattern 'Five-SeveN | Kami'.

    :return: A list of pattern that are special for the skin and a boolean indicating if the list is ordered.
    :rtype: tuple[list[int], bool]
    """

    return [590, 909], False


if __name__ == '__main__':
    exit(1)
