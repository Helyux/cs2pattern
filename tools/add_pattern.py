# DISCLAIMER: This utility was AI-generated. Review thoroughly before use in production.

__author__ = "Codex"
__version__ = "1.0.0"
__date__ = "02.11.2025"
__email__ = ""
__status__ = "Development"


import argparse
import ast
import json
import re
import textwrap
from pathlib import Path
from typing import Iterable, Optional


ROOT = Path(__file__).resolve().parents[1]
PATTERN_FILE = ROOT / "cs2pattern" / "pattern.json"
ICON_FILE = ROOT / "cs2pattern" / "icons.json"
MAX_JSON_LINE = 80
INDENT = "  "


class PatternToolError(Exception):
    """Raised when we cannot perform the requested update."""


def _parse_weapon_entry(entry: str) -> tuple[str, list[int]]:
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


def _sanitize_weapon_patterns(raw_patterns: dict[str, list[int]]) -> tuple[dict[str, list[int]], list[str]]:
    sanitized: dict[str, list[int]] = {}
    notes: list[str] = []

    for weapon, patterns in raw_patterns.items():
        seen: set[int] = set()
        deduped: list[int] = []
        for pattern in patterns:
            if pattern not in seen:
                seen.add(pattern)
                deduped.append(pattern)
        sanitized[weapon] = deduped
        if len(deduped) < len(patterns):
            notes.append(
                f"Removed duplicate pattern ids for '{weapon}': {patterns} -> {deduped}"
            )

    return sanitized, notes


def _load_pattern_data() -> dict:
    if not PATTERN_FILE.exists():
        raise PatternToolError(f"Pattern file not found: {PATTERN_FILE}")

    with PATTERN_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_pattern_data(data: dict) -> None:
    formatted = _format_json(data)
    PATTERN_FILE.write_text(formatted + "\n", encoding="utf-8")


def _load_icon_map() -> dict[str, str]:
    if ICON_FILE.exists():
        return json.loads(ICON_FILE.read_text(encoding="utf-8"))
    return {}


def _write_icon_map(icon_map: dict[str, str]) -> None:
    ICON_FILE.write_text(
        json.dumps(dict(sorted(icon_map.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _normalize_pattern_group_name(skin: str, weapons: Iterable[str], current_name: str, canonical_name: str) -> None:
    if current_name == canonical_name:
        return

    skin_key = skin.lower()
    data = _load_pattern_data()
    skin_entry = data.get(skin_key)
    if not skin_entry:
        return

    changed = False
    for weapon in weapons:
        groups = skin_entry.get(weapon)
        if not groups:
            continue
        for group in groups:
            if group.get("name") == current_name:
                group["name"] = canonical_name
                changed = True

    if changed:
        _write_pattern_data(data)


def _format_json(data, level: int = 0) -> str:

    if isinstance(data, dict):
        if not data:
            return "{}"
        lines: list[str] = ["{"]
        items = sorted(data.items(), key=lambda item: item[0])
        for index, (key, value) in enumerate(items):
            value_repr = _format_json(value, level + 1)
            comma = "," if index < len(items) - 1 else ""
            lines.append(f"{INDENT * (level + 1)}{json.dumps(key)}: {value_repr}{comma}")
        lines.append(f"{INDENT * level}}}")
        return "\n".join(lines)

    if isinstance(data, list):
        if not data:
            return "[]"
        if all(isinstance(item, int) for item in data):
            return _format_int_list(data, level)

        lines = ["["]
        for index, item in enumerate(data):
            item_repr = _format_json(item, level + 1)
            comma = "," if index < len(data) - 1 else ""
            lines.append(f"{INDENT * (level + 1)}{item_repr}{comma}")
        lines.append(f"{INDENT * level}]")
        return "\n".join(lines)

    if isinstance(data, bool):
        return "true" if data else "false"
    if data is None:
        return "null"
    return json.dumps(data)


def _format_int_list(values: list[int], level: int) -> str:
    indent = INDENT * (level + 1)
    content = ", ".join(str(value) for value in values)
    wrapped = textwrap.wrap(
        content,
        width=max(1, MAX_JSON_LINE - len(indent)),
        break_long_words=False,
        break_on_hyphens=False,
    )
    lines = [indent + line for line in wrapped]
    closing_indent = INDENT * level
    return "[\n" + "\n".join(lines) + f"\n{closing_indent}]"


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_file(path: Path, content: str) -> None:
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def _find_helper_block(content: str, helper_name: str) -> tuple[int, int, str]:

    pattern = re.compile(rf"^def {re.escape(helper_name)}\b", re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return -1, -1, ""

    start = match.start()
    next_def_pattern = re.compile(r"^def [A-Za-z0-9_]+\(", re.MULTILINE)
    next_def_match = next_def_pattern.search(content, match.end())
    sentinel_index = content.find("\nif __name__ == '__main__':", match.end())

    if next_def_match is None or (sentinel_index != -1 and sentinel_index < next_def_match.start()):
        end = sentinel_index if sentinel_index != -1 else len(content)
    else:
        end = next_def_match.start()

    return start, end, content[start:end]


def _merge_helper_block(helper_block: str, helper_name: str, skin_key: str, group_name: str,
                        weapon_patterns: dict[str, list[int]], ordered: bool) -> tuple[str, str, str]:

    if "_lookup_first_group" in helper_block:
        updated, canonical_group = _merge_multi_helper_block(
            helper_block,
            helper_name,
            skin_key,
            group_name,
            weapon_patterns,
            ordered,
        )
        return updated, "multi", canonical_group

    if "_lookup_group" in helper_block:
        updated, canonical_group = _merge_single_helper_block(
            helper_block,
            helper_name,
            skin_key,
            group_name,
            weapon_patterns,
            ordered,
        )
        return updated, "single", canonical_group

    raise PatternToolError(
        f"Helper '{helper_name}' exists but cannot be automatically extended. Please adjust it manually."
    )


def _merge_multi_helper_block(helper_block: str, helper_name: str, skin_key: str, group_name: str,
                              weapon_patterns: dict[str, list[int]], ordered: bool) -> tuple[str, str]:

    lookup_pattern = re.compile(
        r"return _lookup_first_group\(\s*weapon_normalized,\s*'(?P<group>[^']+)',\s*skins\s*\)"
    )
    lookup_match = lookup_pattern.search(helper_block)
    if not lookup_match:
        raise PatternToolError(
            f"Unable to locate lookup call for helper '{helper_name}'. Manual intervention required."
        )

    existing_group = lookup_match.group("group")
    canonical_group = existing_group

    lines = helper_block.splitlines()
    assign_pattern = re.compile(r"(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\{\s*$")

    dict_start = dict_end = None
    indent = ""
    var_name = ""

    for index, line in enumerate(lines):
        match = assign_pattern.match(line)
        if match:
            indent = match.group(1)
            var_name = match.group(2)
            dict_start = index
            break

    if dict_start is None:
        raise PatternToolError(
            f"Unable to locate mapping dictionary inside helper '{helper_name}'."
        )

    closing_prefix = f"{indent}}}"
    for index in range(dict_start + 1, len(lines)):
        if lines[index].startswith(closing_prefix):
            dict_end = index
            break

    if dict_end is None:
        raise PatternToolError(
            f"Unable to locate mapping terminator for helper '{helper_name}'."
        )

    dict_text = "\n".join(lines[dict_start:dict_end + 1])

    try:
        literal_mapping = ast.literal_eval(dict_text.split("=", 1)[1].strip())
    except (IndexError, SyntaxError, ValueError) as exc:
        raise PatternToolError(
            f"Failed to parse mapping for helper '{helper_name}'."
        ) from exc

    pattern_data = _load_pattern_data()
    existing_ordered: Optional[bool] = None

    mapping: dict[str, tuple[str, ...]] = {}
    for weapon, skins_value in literal_mapping.items():
        skins_tuple: tuple[str, ...]
        if isinstance(skins_value, str):
            skins_tuple = (skins_value,)
        else:
            skins_tuple = tuple(skins_value)
        normalized_skins = tuple(sorted(set(skins_tuple)))
        mapping[weapon] = normalized_skins
        if existing_ordered is None:
            for skin_option in normalized_skins:
                for group in pattern_data.get(skin_option, {}).get(weapon, []):
                    if group.get("name") == existing_group:
                        existing_ordered = bool(group.get("ordered", False))
                        break
                if existing_ordered is not None:
                    break

    if existing_ordered is None:
        existing_ordered = ordered
    elif existing_ordered != ordered:
        raise PatternToolError(
            f"Helper '{helper_name}' uses ordered={existing_ordered}, requested ordered={ordered}."
        )

    updated_mapping: dict[str, tuple[str, ...]] = dict(mapping)

    changed = False
    for weapon in weapon_patterns:
        existing_skins = updated_mapping.get(weapon, ())
        if skin_key in existing_skins:
            continue
        updated_skins = tuple(sorted(set(existing_skins + (skin_key,))))
        updated_mapping[weapon] = updated_skins
        changed = True

    if not changed:
        return helper_block, canonical_group

    reconstructed: list[str] = [f"{indent}{var_name} = {{"]
    for weapon in sorted(updated_mapping):
        skins_repr = repr(updated_mapping[weapon])
        reconstructed.append(f"{indent}    '{weapon}': {skins_repr},")
    reconstructed.append(f"{indent}}}")

    new_lines = lines[:dict_start] + reconstructed + lines[dict_end + 1:]
    helper_block_has_trailing_newline = helper_block.endswith("\n")
    new_block = "\n".join(new_lines)
    if helper_block_has_trailing_newline:
        new_block += "\n"
    return new_block, canonical_group


def _merge_single_helper_block(helper_block: str, helper_name: str, skin_key: str, group_name: str,
                               weapon_patterns: dict[str, list[int]], ordered: bool) -> tuple[str, str]:

    lookup_pattern = re.compile(
        r"return _lookup_group\(\s*'(?P<skin>[^']+)',\s*'(?P<weapon>[^']+)',\s*'(?P<group>[^']+)'\s*\)"
    )
    match = lookup_pattern.search(helper_block)
    if not match:
        raise PatternToolError(
            f"Unable to locate lookup call for helper '{helper_name}'. Manual intervention required."
        )

    existing_skin = match.group("skin")
    existing_weapon = match.group("weapon")
    existing_group = match.group("group")

    canonical_group = existing_group

    if skin_key != existing_skin:
        raise PatternToolError(
            f"Helper '{helper_name}' uses skin '{existing_skin}', expected '{skin_key}'."
        )

    if len(weapon_patterns) != 1 or existing_weapon not in weapon_patterns:
        raise PatternToolError(
            f"Helper '{helper_name}' handles weapon '{existing_weapon}'. Automatic merge for additional weapons is unsupported."
        )

    # Nothing to change for single-weapon helpers, return block unchanged.
    return helper_block, canonical_group


def add_pattern(skin: str, group_name: str, weapon_patterns: dict[str, list[int]], ordered: bool, overwrite: bool) -> None:
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
    :param overwrite: Replace an existing group if it already exists.
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


def _update_icon_map(group_name: str, icon: Optional[str], overwrite: bool) -> None:
    if not icon:
        return

    icon_map = _load_icon_map()
    existing_icon = icon_map.get(group_name)

    if existing_icon == icon:
        return

    if existing_icon is not None and not overwrite:
        raise PatternToolError(
            f"Icon for group '{group_name}' already exists. Use --overwrite to replace it."
        )

    icon_map[group_name] = icon
    _write_icon_map(icon_map)


def _update_modular_helper(helper_name: str, skin: str, group_name: str,
                           weapon_patterns: dict[str, list[int]], ordered: bool) -> tuple[str, bool, str]:

    modular_path = ROOT / "cs2pattern" / "modular.py"
    content = _read_file(modular_path)

    skin_key = skin.lower()

    helper_start, helper_end, helper_block = _find_helper_block(content, helper_name)
    if helper_start != -1:
        merged_block, helper_kind, canonical_group = _merge_helper_block(
            helper_block,
            helper_name=helper_name,
            skin_key=skin_key,
            group_name=group_name,
            weapon_patterns=weapon_patterns,
            ordered=ordered,
        )

        if merged_block == helper_block:
            return helper_kind, False, canonical_group

        updated_content = content[:helper_start] + merged_block + content[helper_end:]
        _write_file(modular_path, updated_content)
        return helper_kind, False, canonical_group

    public_defs = [
        (match.group(1), match.start())
        for match in re.finditer(r"\ndef\s+([a-zA-Z0-9_]+)\s*\(", content)
        if not match.group(1).startswith("_")
    ]

    insertion_index = content.find("\n\nif __name__ == '__main__':")
    if insertion_index == -1:
        raise PatternToolError("Unable to locate insertion marker in cs2pattern.modular.")

    for name, position in public_defs:
        if name > helper_name:
            insertion_index = position
            break

    helper_kind = "single" if len(weapon_patterns) == 1 else "multi"
    canonical_group = group_name

    if len(weapon_patterns) == 1:
        weapon = next(iter(weapon_patterns.keys()))
        helper_template = f'''
def {helper_name}() -> tuple[list[int], bool]:
    """
    Auto-generated helper for '{skin}' pattern group '{group_name}'.
    """

    return _lookup_group('{skin_key}', '{weapon}', '{group_name}')
'''
        helper_code = "\n" + textwrap.dedent(helper_template)
    else:
        mapping_lines = "\n".join(
            f"        '{weapon}': ('{skin_key}',)," for weapon in weapon_patterns.keys()
        )
        helper_template = f'''
def {helper_name}(weapon: str) -> Optional[tuple[list[int], bool]]:
    """
    Auto-generated helper for '{skin}' pattern group '{group_name}'.
    """

    weapon_options = {
{mapping_lines}
    }

    weapon_normalized = weapon.lower()
    skins = weapon_options.get(weapon_normalized)
    if not skins:
        return None
    return _lookup_first_group(weapon_normalized, '{group_name}', skins)
'''
        helper_code = "\n" + textwrap.dedent(helper_template)

    updated = content[:insertion_index] + helper_code + content[insertion_index:]
    _write_file(modular_path, updated)
    return helper_kind, True, canonical_group


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
    entries = sorted(set(entries))
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
    existing: list[str] = []
    for line in block.splitlines()[1:]:
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.endswith(","):
            cleaned = cleaned[:-1]
        for item in cleaned.split(","):
            name = item.strip()
            if name and name not in existing:
                existing.append(name)

    if helper_name in existing:
        return

    existing.append(helper_name)
    existing = sorted(existing)

    reconstructed = "from cs2pattern import (\n" + "\n".join(f"    {name}," for name in existing) + "\n)"
    updated = content[:start] + reconstructed + "\n" + content[end + 2:]
    _write_file(test_path, updated)


def _append_single_helper_test_case(helper_name: str, skin: str, weapon: str, group_name: str) -> None:

    test_path = ROOT / "tests" / "test_pattern.py"
    content = _read_file(test_path)

    cases_marker = "    def test_simple_helpers(self):\n        cases = [\n"
    start_index = content.find(cases_marker)
    if start_index == -1:
        raise PatternToolError("Unable to locate cases list in TestModularHelpers.")

    list_start = start_index + len(cases_marker)
    list_end = content.find("        ]\n\n        for func, skin, weapon, group_name in cases:\n", list_start)
    if list_end == -1:
        raise PatternToolError("Unable to locate cases terminator in TestModularHelpers.")

    existing_block = content[list_start:list_end]
    entries = [line for line in existing_block.splitlines() if line.strip()]

    new_entry = f"            ({helper_name}, '{skin.lower()}', '{weapon}', '{group_name}'),"

    helper_entries: dict[str, str] = {}

    for entry in entries:
        name_match = re.search(r"\(\s*([a-zA-Z0-9_]+)", entry)
        if not name_match:
            continue
        name = name_match.group(1)
        helper_entries[name] = entry

    helper_entries[helper_name] = new_entry

    sorted_entries = [helper_entries[name] for name in sorted(helper_entries)]
    rebuilt_block = "\n".join(sorted_entries) + ("\n" if sorted_entries else "")

    updated = content[:list_start] + rebuilt_block + content[list_end:]
    _write_file(test_path, updated)


def _append_multi_helper_test(helper_name: str, skin: str, weapons: Iterable[str], group_name: str):

    test_path = ROOT / "tests" / "test_pattern.py"
    content = _read_file(test_path)

    if f"def test_{helper_name}_helper" in content:
        updated = _update_existing_multi_helper_test_cases(
            content,
            helper_name=helper_name,
            skin=skin,
            weapons=weapons,
        )
        if updated != content:
            _write_file(test_path, updated)
        return

    weapon_list = ", ".join(f"'{weapon}'" for weapon in weapons)
    method_body = textwrap.dedent(
        f"""
def test_{helper_name}_helper(self):
    weapons = [{weapon_list}]

    for weapon in weapons:
        with self.subTest(weapon=weapon):
            expected = self._expect_group('{skin.lower()}', weapon, '{group_name}')
            self.assertEqual({helper_name}(weapon), expected)

    self.assertIsNone({helper_name}('unsupported'))
"""
    ).strip("\n")
    method = "\n" + textwrap.indent(method_body, INDENT) + "\n"

    marker = "\n\nif __name__ == '__main__':"
    if marker not in content:
        raise PatternToolError("Unable to locate tests sentinel for insertion.")

    updated = content.replace(marker, "\n" + method + marker, 1)
    _write_file(test_path, updated)


def _update_existing_multi_helper_test_cases(content: str, helper_name: str, skin: str, weapons: Iterable[str]) -> str:

    method_pattern = re.compile(rf"^    def test_{re.escape(helper_name)}_helper\(self\):", re.MULTILINE)
    method_match = method_pattern.search(content)
    if not method_match:
        return content

    start = method_match.start()
    next_method_pattern = re.compile(r"^    def ", re.MULTILINE)
    next_method_match = next_method_pattern.search(content, method_match.end())
    sentinel_index = content.find("\nif __name__ == '__main__':", method_match.end())

    if next_method_match is None or (sentinel_index != -1 and sentinel_index < next_method_match.start()):
        end = sentinel_index if sentinel_index != -1 else len(content)
    else:
        end = next_method_match.start()

    method_block = content[start:end]
    lines = method_block.splitlines()

    assign_pattern = re.compile(r"(\s*)cases\s*=\s*\{\s*$")
    dict_start = dict_end = None
    indent = ""

    for index, line in enumerate(lines):
        match = assign_pattern.match(line)
        if match:
            indent = match.group(1)
            dict_start = index
            break

    if dict_start is None:
        return content

    closing_prefix = f"{indent}}}"
    for index in range(dict_start + 1, len(lines)):
        if lines[index].startswith(closing_prefix):
            dict_end = index
            break

    if dict_end is None:
        return content

    dict_text = "\n".join(lines[dict_start:dict_end + 1])
    try:
        dict_literal = dict_text.split("=", 1)[1].strip()
        cases = ast.literal_eval(dict_literal)
    except (IndexError, SyntaxError, ValueError):
        return content

    skin_value = skin.lower()
    updated_cases: dict[str, str] = {weapon: cases[weapon] for weapon in cases}
    changed = False

    for weapon in weapons:
        if updated_cases.get(weapon) == skin_value:
            continue
        updated_cases[weapon] = skin_value
        changed = True

    if not changed:
        return content

    reconstructed: list[str] = [f"{indent}cases = {{"]
    for weapon in sorted(updated_cases):
        reconstructed.append(f"{indent}    '{weapon}': '{updated_cases[weapon]}',")
    reconstructed.append(f"{indent}}}")

    new_lines = lines[:dict_start] + reconstructed + lines[dict_end + 1:]
    block_has_trailing_newline = method_block.endswith("\n")
    new_block = "\n".join(new_lines)
    if block_has_trailing_newline:
        new_block += "\n"

    fallback_pattern = re.compile(
        rf"self\.assertEqual\(\s*{re.escape(helper_name)}\('unsupported'\),\s*\(\[\],\s*(?:True|False)\s*\)\s*\)"
    )
    new_block = fallback_pattern.sub(
        f"self.assertIsNone({helper_name}('unsupported'))",
        new_block,
    )

    return content[:start] + new_block + content[end:]


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
    parser.add_argument(
        "--icon",
        help="Optional icon or emoji to associate with the pattern group inside icons.json.",
    )

    args = parser.parse_args()
    normalization_notes: list[str] = []

    try:
        raw_patterns = dict(_parse_weapon_entry(entry) for entry in args.weapon)
        weapon_patterns, normalization_notes = _sanitize_weapon_patterns(raw_patterns)
        helper_msg = ""
        canonical_group = args.name

        if args.helper:
            helper_kind, helper_created, canonical_group = _update_modular_helper(
                helper_name=args.helper,
                skin=args.skin,
                group_name=args.name,
                weapon_patterns=weapon_patterns,
                ordered=args.ordered,
            )
            _update_init(args.helper)
            _update_test_import(args.helper)
            if helper_kind == "multi":
                _append_multi_helper_test(
                    args.helper,
                    args.skin,
                    weapon_patterns.keys(),
                    canonical_group,
                )
            else:
                weapon = next(iter(weapon_patterns.keys()))
                _append_single_helper_test_case(args.helper, args.skin, weapon, canonical_group)

        add_pattern(
            skin=args.skin,
            group_name=canonical_group,
            weapon_patterns=weapon_patterns,
            ordered=args.ordered,
            overwrite=args.overwrite,
        )

        if args.helper:
            _normalize_pattern_group_name(
                args.skin,
                weapon_patterns.keys(),
                args.name,
                canonical_group,
            )
            action = "created" if helper_created else "updated"
            helper_msg = f" Helper '{args.helper}' {action}."

        _update_icon_map(canonical_group, args.icon, args.overwrite)
    except PatternToolError as exc:
        parser.error(str(exc))
    except json.JSONDecodeError as exc:
        parser.error(f"Failed to parse pattern.json: {exc}")

    for note in normalization_notes:
        print(note)

    icon_msg = f" Icon set to {args.icon}." if args.icon else ""
    print(
        f"Pattern group '{canonical_group}' added for skin '{args.skin.lower()}'.{helper_msg}{icon_msg}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
