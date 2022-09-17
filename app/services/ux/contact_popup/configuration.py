from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    api_url: str
    content: str
    contact_type: str
    horizontal_pos: str
    vertical_pos: str
    event_type: str
    save_event: bool
    dark_theme: bool

    @validator("api_url")
    def validate_api_url(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("content")
    def validate_content(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("event_type")
    def validate_event_type(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value
