from pathlib import Path

import pytest
from pydantic import ValidationError
from emojis.db import get_emoji_by_code

from twemoji_api.api import (
    get_emoji_code_points,
    get_emoji_path,
    get_emoji_url,
    Twemoji,
)


# ---------------------------------------------------------------------------
# Basic behavior
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "emoji, expected",
    [
        ("😂", ["1f602"]),
        ("🔥", ["1f525"]),
        ("👏🏻", ["1f44f"]),
    ]
)
def test_get_emoji_code_points(emoji, expected):
    assert get_emoji_code_points(emoji) == expected


def test_get_emoji_path_basic():
    path = Path(__file__).parent / "twemoji_api/assets/72x72/1f602.png"
    assert get_emoji_path("😂") == path


def test_get_emoji_url_basic():
    url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f602.png"
    assert get_emoji_url("😂") == url


def test_get_emoji_url_svg():
    url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/1f602.svg"
    assert get_emoji_url("😂", "svg") == url


# ---------------------------------------------------------------------------
# Twemoji wrapper
# ---------------------------------------------------------------------------

def test_twemoji_code_points():
    assert Twemoji("😂").code_points == ["1f602"]


def test_twemoji_path():
    path = Path(__file__).parent / "twemoji_api/assets/72x72/1f602.png"
    assert Twemoji("😂").path == path


def test_twemoji_url():
    url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f602.png"
    assert Twemoji("😂").url == url


def test_twemoji_svg_url():
    url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/1f602.svg"
    assert Twemoji("😂", "svg").url == url


def test_twemoji_init_equivalency():
    """Emoji instance and raw emoji string must behave identically."""
    t1 = Twemoji("😂")
    t2 = Twemoji(get_emoji_by_code("😂"))
    assert t1.emoji == t2.emoji


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value",
    ["anything", "😭😂", "", "not-an-emoji"]
)
def test_twemoji_invalid_inputs(value):
    """Invalid emoji inputs must raise ValidationError."""
    with pytest.raises(ValidationError):
        Twemoji(value)


def test_twemoji_invalid_extension():
    """Invalid file extensions must raise ValidationError."""
    with pytest.raises(ValidationError):
        Twemoji("😂", "jpeg")


def test_get_emoji_path_invalid_extension():
    """Function-level invalid extension must raise ValidationError."""
    with pytest.raises(ValidationError):
        get_emoji_path("😂", "jpeg")


# ---------------------------------------------------------------------------
# Similarity / fallback
# ---------------------------------------------------------------------------

def test_fallback_skintone():
    """
    If the fully specific version exists (e.g. 1f44f-1f3fb.png),
    it must be returned.
    Otherwise, fallback to the base version (1f44f.png).
    """
    path = get_emoji_path("👏🏻")
    assert path is not None
    assert path.name in ["1f44f-1f3fb.png", "1f44f.png"]


def test_fallback_best_match():
    """
    Incomplete codepoints (e.g. 👏 instead of 👏🏻) must still match a valid file.
    """
    base_stem = Twemoji("👏🏻").path.stem
    fallback = get_emoji_path("👏")
    assert fallback is not None
    assert fallback.stem in [base_stem, "1f44f"]


@pytest.mark.parametrize("emoji", ["☺️", "👁️‍🗨️"])
def test_unicode_variants(emoji):
    """Variation selectors and ZWJ sequences must resolve correctly."""
    path = get_emoji_path(emoji)
    assert path is not None and path.exists()


# ---------------------------------------------------------------------------
# Full DB coverage
# ---------------------------------------------------------------------------

def test_all_emojis_have_valid_files():
    """
    Ensures that every emoji in emojis.db resolves to a real file.
    """
    from emojis.db.db import EMOJI_DB

    for emoji in EMOJI_DB:
        path = get_emoji_path(emoji)
        assert path is not None and path.exists()
