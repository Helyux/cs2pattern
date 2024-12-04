__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.12.2024"
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


def _normalize_input(market_hash: str, pattern: int) -> Optional[tuple[str, str, int]]:
    """
    Normalize and validate CS2 item input.

    :param market_hash: The market hash of the item.
    :type market_hash: str

    :param pattern: The pattern, which should be numeric and between 0-1000 (inclusive).
    :type pattern: int

    :return: A tuple of the normalized weapon, skin and pattern or None if we failed normalizing.
    :rtype: Optional[tuple[str, str, int]]
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

    return weapon, skin, pattern


def _check_special(normalized_data: tuple[str, str, int]) -> Optional[tuple[str, int]]:
    """
    Check if the normalized data matches a special pattern.

    :param normalized_data: The normalized weapon, skin, and pattern tuple.
    :type normalized_data: tuple[str, str, int]

    :return: A tuple with the pattern name and index, -1 if unordered, or None if no match is found.
    :rtype: Optional[tuple[str, int]]
    """

    weapon, skin, pattern = normalized_data

    # Check if skin and weapon exist in the pattern data
    if skin not in SPECIAL_PATTERN or weapon not in SPECIAL_PATTERN[skin]:
        return None

    groups = SPECIAL_PATTERN[skin][weapon]
    if isinstance(groups, dict):
        groups = [groups]

    for group in groups:
        if pattern in group.get('pattern', []):
            index = group['pattern'].index(pattern) + 1 if group.get('ordered') else -1
            return group['name'], index

    return None


def check_rare(market_hash: str, pattern: int) -> tuple[bool, Optional[tuple[str, int]]]:
    """
    Determine if the given item is rare based on market hash and pattern.

    :param market_hash: The market hash of the item.
    :type market_hash: str
    :param pattern: The pattern to check for rarity.
    :type pattern: int

    :return: A tuple indicating if the item is rare and the special pattern details if any.
    :rtype: tuple[bool, Optional[tuple[str, int]]]
    """

    normalized = _normalize_input(market_hash, pattern)
    if not normalized:
        return False, None

    special = _check_special(normalized)

    return (True, special) if special else (False, None)


def get_pattern_dict() -> dict:
    """
    Retrieve the dictionary containing special patterns.

    :return: The special pattern dictionary.
    :rtype: dict
    """

    return SPECIAL_PATTERN


if __name__ == '__main__':
    exit(1)
