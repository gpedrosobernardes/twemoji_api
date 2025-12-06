import typing

from emojis.db import Emoji, get_emoji_by_code
from pydantic import BaseModel, field_validator

from twemoji_api.enum import PhotoType


class EmojiParams(BaseModel):
    emoji: typing.Union[Emoji, str]

    @field_validator("emoji", mode="before")
    def load_emoji(cls, v):
        # se já for Emoji, deixa como está
        if isinstance(v, Emoji):
            return v
        # se for código, converte
        return get_emoji_by_code(v)


class ExtensionParams(BaseModel):
    extension: PhotoType