from pydantic import BaseModel, validator, field_validator
from typing import Optional, Union
from datetime import datetime
from tracardi.service.plugin.domain.config import PluginConfig


class Card(BaseModel):
    name: str
    desc: Optional[str] = None
    urlSource: Optional[str] = None
    coordinates: Optional[str] = None
    due: Optional[Union[str, datetime]] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Card name cannot be empty")
        return value


class Config(PluginConfig):
    board_url: str
    list_name: str
    list_id: str = None
    card: Card

    @field_validator("board_url")
    @classmethod
    def board_url_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Board URL cannot be empty")
        return value

    @field_validator("list_name")
    @classmethod
    def list_name_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("List name cannot be empty")
        return value
