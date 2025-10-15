__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "15.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import argparse
import ast
import json
import re
import textwrap
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
PATTERN_FILE = ROOT / "cs2pattern" / "pattern.json"


class PatternToolError(Exception):
    """Raised when we cannot perform the requested update."""


def _parse_weapon_entry(entry: str) -> Tuple[str, List[int]]:
    """
    Parse a weapon specification argument.

    :param entry: String in the format 'weapon:pattern1 pattern2 ...'
    :type entry: str

    :return: Normalized weapon label and associated pattern list.
    :rtype: tuple[str, list[int]]
    """

    if ":" not in entry:
        raise PatternToolError("Weapon entries must use the format 'weapon:pattern1 pattern2 ...'")

    weapon, pattern_spec = entry.split(":", 1)
    weapon_normalized = weapon.strip().lower()

    if not weapon_normalized:
        raise PatternToolError("Weapon name cannot be empty.")

    pattern_tokens = [token for token in re.split(r"[,\s]+", pattern_spec.strip()) if token]
    if not pattern_tokens:
        raise PatternToolError(f"No patterns provided for weapon '{weapon_normalized}'.")

    try:
        patterns = [int(token) for token in pattern_tokens]
    except ValueError as exc:
        raise PatternToolError("Pattern identifiers must be integers.") from exc

    for pattern in patterns:
        if not (0 <= pattern <= 1000):
            raise PatternToolError(f"Pattern '{pattern}' is outside the valid range (0-1000).")

    return weapon_normalized, patterns


def _load_pattern_data() -> Dict:
    if not PATTERN_FILE.exists():
        raise PatternToolError(f"Pattern file not found: {PATTERN_FILE}")

    with PATTERN_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_pattern_data(data: Dict) -> None:
    with PATTERN_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_file(path: Path, content: str) -> None:
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def add_pattern(
    skin: str,
    group_name: str,
    weapon_patterns: Dict[str, List[int]],
    ordered: bool,
    overwrite: bool,
) -> None:
    """
    Insert or update a pattern group inside pattern.json.

    :param skin: Skin identifier.
    :type skin: str
    :param group_name: Name of the pattern group to create.
    :type group_name: str
    :param weapon_patterns: Mapping from weapon label to pattern ids.
    :type weapon_patterns: dict[str, list[int]]
    :param ordered: Whether pattern ids are ordered.
    :type ordered: bool
    :param overwrite: Replace existing group if it already exists.
    :type overwrite: bool
    """

    skin_key = skin.lower()
    data = _load_pattern_data()

    skin_entry = data.setdefault(skin_key, {})

    for weapon, patterns in weapon_patterns.items():
        weapon_groups = skin_entry.setdefault(weapon, [])
        existing_index = next(
            (index for index, group in enumerate(weapon_groups) if group.get("name") == group_name),
            None,
        )

        new_group = {
            "name": group_name,
            "pattern": patterns,
            "ordered": ordered,
        }

        if existing_index is None:
            weapon_groups.append(new_group)
        elif overwrite:
            weapon_groups[existing_index] = new_group
        else:
            raise PatternToolError(
                f"Group '{group_name}' already exists for '{skin_key}' / '{weapon}'. "
                "Use --overwrite to replace it."
            )

    _write_pattern_data(data)


def _update_modular_helper(
    helper_name: str,
    skin: str,
    group_name: str,
    weapon_patterns: Dict[str, List[int]],
    ordered: bool,
) -> None:
    modular_path = ROOT / "cs2pattern" / "modular.py"
    content = _read_file(modular_path)

    if f"def {helper_name}" in content:
        raise PatternToolError(f"Helper '{helper_name}' already exists in cs2pattern.modular.")

    insertion_marker = "\n\nif __name__ == '__main__':"
    marker_index = content.find(insertion_marker)
    if marker_index == -1:
        raise PatternToolError("Unable to locate insertion marker in cs2pattern.modular.")

    skin_key = skin.lower()
    ordered_literal = "True" if ordered else "False"

    if len(weapon_patterns) == 1:
        weapon = next(iter(weapon_patterns.keys()))
        helper_code = textwrap.dedent(
            f"""

def {helper_name}() -> tuple[list[int], bool]:
    \"\"\"
    Auto-generated helper for '{skin}' pattern group '{group_name}'.
    \"\"\"

    return _lookup_group('{skin_key}', '{weapon}', '{group_name}')
"""
        )
    else:
        mapping_lines = "\n".join(
            f"        '{weapon}': ('{skin_key}',)," for weapon in weapon_patterns.keys()
        )
        helper_code = textwrap.dedent(
            f"""

def {helper_name}(weapon: str) -> tuple[list[int], bool]:
    \"\"\"
    Auto-generated helper for '{skin}' pattern group '{group_name}'.
    \"\"\"

    weapon_normalized = weapon.lower()
    weapon_options = {{
{mapping_lines}
    }}

    skins = weapon_options.get(weapon_normalized)
    if not skins:
        return [], {ordered_literal}
    return _lookup_first_group(weapon_normalized, '{group_name}', skins, {ordered_literal})
"""
        )

    updated = content[:marker_index] + helper_code + insertion_marker + content[marker_index + len(insertion_marker):]
    _write_file(modular_path, updated)


def _update_init(helper_name: str) -> None:
    init_path = ROOT / "cs2pattern" / "__init__.py"
    content = _read_file(init_path)

    start = content.find("__all__ = [")
    if start == -1:
        raise PatternToolError("Unable to locate __all__ definition in cs2pattern.__init__.")

    list_start = content.find("[", start)
    list_end = content.find("]\n", list_start)
    if list_end == -1:
        raise PatternToolError("Unable to parse __all__ list.")

    list_text = content[list_start:list_end + 1]
    entries = ast.literal_eval(list_text)
    if helper_name in entries:
        return

    entries.append(helper_name)
    new_list = "__all__ = [\n" + "".join(f"    '{entry}',\n" for entry in entries) + "]\n"
    updated = content[:start] + new_list + content[list_end + 2:]
    _write_file(init_path, updated)


def _update_test_import(helper_name: str) -> None:
    test_path = ROOT / "tests" / "test_pattern.py"
    content = _read_file(test_path)

    start = content.find("from cs2pattern import (")
    if start == -1:
        raise PatternToolError("Unable to locate import block in tests/test_pattern.py.")

    end = content.find(")\n", start)
    if end == -1:
        raise PatternToolError("Unable to locate import block terminator in tests/test_pattern.py.")

    block = content[start:end]
    existing = []
    for line in block.splitlines()[1:]:
        stripped = line.strip().rstrip(",")
        if not stripped:
            continue
        if stripped not in existing:
            existing.append(stripped)

    if helper_name in existing:
        return

    insert_index = next(
        (index for index, name in enumerate(existing) if helper_name < name),
        len(existing),
    )
    existing.insert(insert_index, helper_name)

    reconstructed = "from cs2pattern import (\n" + "\n".join(f"    {name}," for name in existing) + "\n)"
    updated = content[:start] + reconstructed + "\n" + content[end + 2:]
    _write_file(test_path, updated)


def _append_single_helper_test_case(helper_name: str, skin: str, weapon: str, group_name: str) -> None:
    test_path = ROOT / "tests" / "test_pattern.py"
    content = _read_file(test_path)

    marker = "\n        ]\n\n        for func, skin, weapon, group_name in cases:\n"
    if marker not in content:
        raise PatternToolError("Unable to locate cases list in TestModularHelpers.")

    insertion = (
        f"\n            ({helper_name}, '{skin.lower()}', '{weapon}', '{group_name}'),"
    )
    updated = content.replace(marker, insertion + marker, 1)
    _write_file(test_path, updated)


def _append_multi_helper_test(
    helper_name: str,
    skin: str,
    weapons: Iterable[str],
    group_name: str,
    ordered: bool,
) -> None:
    test_path = ROOT / "tests" / "test_pattern.py"
    content = _read_file(test_path)

    if f"def test_{helper_name}_helper" in content:
        return

    weapon_list = ", ".join(f"'{weapon}'" for weapon in weapons)
    ordered_literal = "True" if ordered else "False"
    method = textwrap.dedent(
        f"""

    def test_{helper_name}_helper(self):
        weapons = [{weapon_list}]

        for weapon in weapons:
            with self.subTest(weapon=weapon):
                expected = self._expect_group('{skin.lower()}', weapon, '{group_name}')
                self.assertEqual({helper_name}(weapon), expected)

        self.assertEqual({helper_name}('unsupported'), ([], {ordered_literal}))
"""
    )

    marker = "\n\nif __name__ == '__main__':"
    if marker not in content:
        raise PatternToolError("Unable to locate tests sentinel for insertion.")

    updated = content.replace(marker, method + marker, 1)
    _write_file(test_path, updated)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Maintenance helper for adding or updating entries inside pattern.json.",
    )
    parser.add_argument(
        "--skin",
        required=True,
        help="Skin identifier (matches the keys already present inside pattern.json).",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Pattern group name to create or update.",
    )
    parser.add_argument(
        "--weapon",
        action="append",
        required=True,
        help="Weapon + pattern specification. Example: \"ak-47:661 670 955\". "
             "Repeat for multiple weapons.",
    )
    parser.add_argument(
        "--ordered",
        action="store_true",
        help="Flag the pattern list as ordered (defaults to False).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing group with the provided data instead of failing.",
    )
    parser.add_argument(
        "--helper",
        help="Optional helper name to add to cs2pattern.modular and expose via the package API.",
    )

    args = parser.parse_args()

    try:
        weapon_patterns = dict(_parse_weapon_entry(entry) for entry in args.weapon)
        add_pattern(
            skin=args.skin,
            group_name=args.name,
            weapon_patterns=weapon_patterns,
            ordered=args.ordered,
            overwrite=args.overwrite,
        )
        helper_msg = ""
        if args.helper:
            _update_modular_helper(
                helper_name=args.helper,
                skin=args.skin,
                group_name=args.name,
                weapon_patterns=weapon_patterns,
                ordered=args.ordered,
            )
            _update_init(args.helper)
            _update_test_import(args.helper)
            if len(weapon_patterns) == 1:
                weapon = next(iter(weapon_patterns.keys()))
                _append_single_helper_test_case(args.helper, args.skin, weapon, args.name)
            else:
                _append_multi_helper_test(
                    args.helper,
                    args.skin,
                    weapon_patterns.keys(),
                    args.name,
                    args.ordered,
                )
            helper_msg = f" Helper '{args.helper}' created."
    except PatternToolError as exc:
        parser.error(str(exc))
    except json.JSONDecodeError as exc:
        parser.error(f"Failed to parse pattern.json: {exc}")

    print(
        f"Pattern group '{args.name}' added for skin '{args.skin.lower()}'.{helper_msg}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
