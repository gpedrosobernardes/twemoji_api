from pathlib import Path

import pytest

from twemoji_api import (
    get_emoji_path,
    get_emoji_url,
)

from emoji_data_python import emoji_data, EmojiChar


# ---------------------------------------------------------------------------
# Basic behavior
# ---------------------------------------------------------------------------

def test_get_emoji_path_basic():
    path = Path(__file__).parent.absolute() / "twemoji_api/assets/72x72/1f602.png"
    assert get_emoji_path("😂") == path


def test_get_emoji_url_basic():
    url = "https://raw.githubusercontent.com/jdecked/twemoji/master/assets/72x72/1f602.png"
    assert get_emoji_url("😂") == url


def test_get_emoji_url_svg():
    url = "https://raw.githubusercontent.com/jdecked/twemoji/master/assets/svg/1f602.svg"
    assert get_emoji_url("😂", "svg") == url


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def test_get_emoji_path_invalid_extension():
    """Function-level invalid extension must raise ValueError."""
    with pytest.raises(ValueError, match="Invalid extension"):
        get_emoji_path("😂", "jpeg")


def test_get_emoji_path_not_found():
    """Missing emoji must raise ValueError."""
    with pytest.raises(ValueError, match="Emoji not found"):
        get_emoji_path("invalid")


# ---------------------------------------------------------------------------
# Unicode variants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("emoji", ["☺️", "👁️‍🗨️"])
def test_unicode_variants(emoji):
    """Variation selectors and ZWJ sequences must resolve correctly."""
    path = get_emoji_path(emoji)
    assert path is not None and path.exists()


# ---------------------------------------------------------------------------
# Full DB coverage
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("emoji", emoji_data)
def test_all_emojis_have_valid_files(emoji: EmojiChar):
    """
    Ensures that every emoji in emoji_data_python resolves to a real file.
    All emojis should now be present in assets.
    """
    path = get_emoji_path(emoji.char)
    assert path is not None and path.exists()
