<div id="shields" align="center">

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Downloads][downloads-shield]][downloads-url]
[![GPLv3 License][license-shield]][license-url]
</div>

# cs2pattern

## Overview

`cs2pattern` is a python package used to identify different rare pattern from counter-strike skins given a pattern number.

## Installation

```bash
pip install cs2pattern
```

## Usage

### Quick start

To check if your skin has a rare pattern:

```python
from cs2pattern import check_rare

# Provide full item name and pattern number
is_rare, details = check_rare("★ Karambit | Case Hardened (Factory New)", 269)
if is_rare:
    rare_name, rank = details
    print(f"Rare pattern: {rare_name} (rank {rank})")

#=> Rare pattern: gem_blue (rank 5)
```

### Modular helpers

When you already know the skin family you care about, import the helper functions:

```python
from cs2pattern import gem_black

patterns, ordered = gem_black("skeleton knife")
print(f"Patterns: {patterns} / Ordered: {ordered}")

#=> Patterns: [446, 791, 497, 28] / Ordered: True
```

### Raw catalog access

Helper names match the pattern groups inside `pattern.json`, so you can discover what is available by calling `get_pattern_dict()` and inspecting the keys.

```python
from cs2pattern import get_pattern_dict

catalog = get_pattern_dict()
scorched_ursus = catalog["scorched"]["ursus knife"][0]
print(scorched_ursus["pattern"])

#=> [446, 791]
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
[downloads-shield]: https://img.shields.io/pepy/dt/cs2pattern?style=for-the-badge
[downloads-url]: https://pepy.tech/project/cs2pattern
[license-shield]: https://img.shields.io/badge/License-GPLv3-red.svg?style=for-the-badge
[license-url]: https://github.com/Helyux/cs2pattern/blob/master/LICENSE
