# Twemoji API

![PyPI](https://img.shields.io/pypi/v/twemoji-api)
![Python](https://img.shields.io/pypi/pyversions/twemoji-api)
![License](https://img.shields.io/github/license/gpedrosobernardes/twemoji_api)
![Downloads](https://img.shields.io/pypi/dm/twemoji-api)

A lightweight utility for resolving emojis into local asset paths and Twemoji URLs.
Supports **PNG** and **SVG** assets.

## Features

* Resolve local Twemoji asset paths
* Resolve URLs for PNG/SVG assets

## Installation

```bash
pip install twemoji-api
```

## Usage

### Basic

```python
from twemoji_api.api import get_emoji_path, get_emoji_url

print(get_emoji_path("🔥"))
print(get_emoji_url("🔥"))
```

## API Reference

### `get_extension_folder(extension)`

Returns the asset folder (`72x72` or `svg`).

### `get_emoji_path(emoji, extension="png")`

Returns the local file path for an emoji.

### `get_emoji_url(emoji, extension="png")`

Returns the Twemoji GitHub URL for the asset.

## License

MIT

## Twemoji Attribution

This project includes graphics from Twemoji.
Copyright 2019 Twitter, Inc and other contributors.
Licensed under CC-BY 4.0:
[https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)
No changes were made.