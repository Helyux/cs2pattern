# Tools Overview

## `add_pattern.py`

`add_pattern.py` is a maintenance helper that keeps `pattern.json`, the modular helper functions, and the test suite in sync when you add or update CS2 pattern metadata.

### Parameters

| Flag | Required | Description |
| --- | --- | --- |
| `--skin` | Yes | Skin identifier (as used in `pattern.json`, case-insensitive). |
| `--name` | Yes | Name of the pattern group to create or update. |
| `--weapon` | Yes (repeatable) | Weapon + pattern specification in the form `weapon:pattern1 pattern2 ...`. You can repeat this flag to cover multiple weapons under the same group. |
| `--ordered` | No | Marks the pattern list as ordered (defaults to `False`). |
| `--overwrite` | No | Replace an existing group instead of failing when the group already exists. |
| `--helper` | No | Optional helper name. When provided, the script generates a convenience wrapper in `cs2pattern.modular`, exposes it via `cs2pattern.__all__`, and adds matching unit tests. |

### Examples

Add a new unordered pattern group for a single weapon:

```bash
python3 tools/add_pattern.py --skin "Case Hardened" --name blaze_v2 --weapon "ak-47:123 456 789"
```

Add an ordered multi-weapon group and auto-generate the helper/tests:

```bash
python3 tools/add_pattern.py --skin "Marble Fade" --name fire_and_ice_v2 --weapon "bayonet:12 34 56" --weapon "karambit:78 90" --ordered --helper fire_and_ice_v2
```

Update an existing group by overwriting its data:

```bash
python3 tools/add_pattern.py --skin "Moonrise" --name star --weapon "glock-18:58 59 66 90" --ordered --overwrite
```

After running the tool, confirm the repository still passes its checks (e.g. `python3 -m pytest`) and review the diff before committing.***
