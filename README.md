<div id="shields" align="center">

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Downloads][downloads-shield]][downloads-url]
[![GPLv3 License][license-shield]][license-url]
[![Xing][xing-shield]][xing-url]
</div>

# cs2pattern

## Overview

`cs2pattern` is a python package used for working with cs2 paint seeds, aka pattern.

## Installation

```bash
pip install cs2pattern
```

## Usage

### Quick start

```python
from cs2pattern import check_rare

is_rare, details = check_rare("★ Karambit | Case Hardened (Factory New)", 941)
if is_rare:
    pattern_name, index = details
    print(f"Rare pattern: {pattern_name} (index {index})")
else:
    print("Nothing special here.")
```

### Modular helpers

When you already know the skin family you care about, import the helper functions:

```python
from cs2pattern import gem_black

patterns, ordered = gem_black("skeleton knife")
print("Patterns:", patterns)
print("Ordered:", ordered)
```

### Raw catalog access

Helper names match the pattern groups inside `pattern.json`, so you can discover what is available by calling `get_pattern_dict()` and inspecting the keys.

```python
from cs2pattern import get_pattern_dict

catalog = get_pattern_dict()
scorched_ursus = catalog["scorched"]["ursus knife"][0]
print(scorched_ursus["pattern"])
```

## Contributing
Contributions are welcome! Open an issue or submit a pull request.

## License
GPLv3 License. See the LICENSE file for details.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Helyux/cs2pattern.svg?style=for-the-badge
[contributors-url]: https://github.com/Helyux/cs2pattern/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Helyux/cs2pattern.svg?style=for-the-badge
[forks-url]: https://github.com/Helyux/cs2pattern/network/members
[stars-shield]: https://img.shields.io/github/stars/Helyux/cs2pattern.svg?style=for-the-badge
[stars-url]: https://github.com/Helyux/cs2pattern/stargazers
[issues-shield]: https://img.shields.io/github/issues/Helyux/cs2pattern.svg?style=for-the-badge
[issues-url]: https://github.com/Helyux/cs2pattern/issues
[downloads-shield]: https://img.shields.io/pypi/dm/cs2pattern.svg?style=for-the-badge
[downloads-url]: https://pypi.org/project/cs2pattern/
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge
[license-url]: https://github.com/Helyux/cs2pattern/blob/master/LICENSE
[xing-shield]: https://img.shields.io/static/v1?style=for-the-badge&message=Xing&color=006567&logo=Xing&logoColor=FFFFFF&label
[xing-url]: https://www.xing.com/profile/Lukas_Mahler10
