__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "02.11.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import json
import os
import re
from dataclasses import dataclass
from typing import Optional

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "pattern.json")
with open(json_path, "r") as file:
    SPECIAL_PATTERN = json.load(file)


@dataclass(frozen=True)
class PatternInfo:
    """
    Normalized lookup result including rarity status and ordering metadata.
    """

    weapon: Optional[str]
    skin: Optional[str]
    pattern: Optional[int]
    is_rare: bool
    group: Optional[str]
    ordered: bool
    order: Optional[tuple[int, int]]


def _normalize_input(market_hash: str, pattern: int) -> Optional[tuple[str, str, int]]:
    """
    Normalize and validate CS2 item input.

    :param market_hash: The market hash of the item.
    :type market_hash: str

    :param pattern: The pattern, which should be numeric and between 0-1000 (inclusive).
    :type pattern: int

    :return: A tuple of the normalized weapon, skin and pattern, or None if we failed to normalize.
    :rtype: Optional[tuple[str, str, int]]
    """

    # Normalize market_hash
    market_hash = re.sub(r"\s+", " ", market_hash.replace("★ ", "").lower()).strip()

    # Extract weapon and skin
    if " | " not in market_hash:
        return None

    weapon, skin = market_hash.split(" | ", 1)
    skin = re.sub(r"\s*\(.*?\)$", "", skin).strip()

    # Validate pattern
    if not (0 <= pattern <= 1000):
        return None

    return weapon, skin, pattern


def _match_group(normalized_data: tuple[str, str, int]) -> Optional[tuple[str, bool, Optional[int], Optional[int]]]:
    """
    Match the normalized data against the known rare pattern groups.

    :param normalized_data: The normalized weapon, skin, and pattern tuple.
    :type normalized_data: tuple[str, str, int]

    :return: Tuple with pattern group name, ordered flag, optional rank, and total if ordered; None if no match.
    :rtype: Optional[tuple[str, bool, Optional[int], Optional[int]]]
    """

    weapon, skin, pattern = normalized_data

    # Check if skin and weapon exist in the pattern data
    if skin not in SPECIAL_PATTERN or weapon not in SPECIAL_PATTERN[skin]:
        return None

    groups = SPECIAL_PATTERN[skin][weapon]

    for group in groups:
        patterns = list(group.get('pattern', []))
        if pattern in patterns:
            ordered = bool(group.get('ordered', False))
            if ordered:
                rank = patterns.index(pattern) + 1
                total = len(patterns)
            else:
                rank = None
                total = None
            return group.get('name'), ordered, rank, total

    return None


def check_rare(market_hash: str, pattern: int) -> PatternInfo:
    """
    Determine if the given item is rare based on market hash and pattern.

    :param market_hash: The market hash of the item.
    :type market_hash: str
    :param pattern: The pattern to check for rarity.
    :type pattern: int

    :return: Structured Pattern info, describing rarity, matching group, ordering, and other details.
    :rtype: PatternInfo
    """

    normalized = _normalize_input(market_hash, pattern)
    if not normalized:
        return PatternInfo(
            weapon=None,
            skin=None,
            pattern=None,
            is_rare=False,
            group=None,
            ordered=False,
            order=None,
        )

    special = _match_group(normalized)

    if not special:
        weapon, skin, normalized_pattern = normalized
        return PatternInfo(
            weapon=weapon,
            skin=skin,
            pattern=normalized_pattern,
            is_rare=False,
            group=None,
            ordered=False,
            order=None,
        )

    group_name, ordered, rank, total = special
    order_info = (rank, total) if ordered and rank is not None and total is not None else None
    weapon, skin, normalized_pattern = normalized
    return PatternInfo(
        weapon=weapon,
        skin=skin,
        pattern=normalized_pattern,
        is_rare=True,
        group=group_name,
        ordered=ordered,
        order=order_info,
    )


def get_pattern_dict() -> dict:
    """
    Retrieve the dictionary containing special patterns.

    :return: The special pattern dictionary.
    :rtype: dict
    """

    return SPECIAL_PATTERN


if __name__ == '__main__':
    exit(1)
