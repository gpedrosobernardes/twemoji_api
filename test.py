from pathlib import Path

import pytest
from pydantic import ValidationError

from twemoji_api.api import get_emoji_file_name, get_emoji_path, Twemoji, get_emoji_url
from emojis.db import get_emoji_by_code


def test_get_emoji_file_name():
    assert get_emoji_file_name("😂") == "1f602"


def test_get_emoji_path():
    path = Path(__file__).parent / "source/twemoji_api/assets/72x72/1f602.png"
    assert get_emoji_path("😂") == path


def test_get_emoji_url():
    png_url = 'https://github.com/jdecked/twemoji/blob/main/assets/72x72/1f602.png'
    assert get_emoji_url("😂") == png_url
    svg_url = 'https://github.com/jdecked/twemoji/blob/main/assets/svg/1f602.svg'
    assert get_emoji_url("😂", "svg") == svg_url


def test_file_name():
    assert Twemoji("😂").file_name == "1f602"


def test_path():
    path = Path(__file__).parent / "source/twemoji_api/assets/72x72/1f602.png"
    assert Twemoji("😂").path == path


def test_url():
    png_url = 'https://github.com/jdecked/twemoji/blob/main/assets/72x72/1f602.png'
    assert Twemoji("😂").url == png_url
    svg_url = 'https://github.com/jdecked/twemoji/blob/main/assets/svg/1f602.svg'
    assert Twemoji("😂", "svg").url == svg_url


def test_twemoji_init():
    emoji_1 = Twemoji("😂")
    emoji_2 = Twemoji(get_emoji_by_code("😂"))
    assert emoji_1.emoji == emoji_2.emoji


def test_twemoji_init_not_emoji():
    with pytest.raises(ValidationError):
        Twemoji("anything")


def test_twemoji_invalid_extension():
    with pytest.raises(ValidationError):
        Twemoji("😂", "jpeg")


def test_get_emoji_path_invalid_extension():
    with pytest.raises(ValidationError):
        get_emoji_path("😂", "jpeg")