from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    api_url: str
    title: str
    message: str
    lifetime: str
    horizontal_position: str
    vertical_position: str
    event_type: str
    save_event: bool
    dark_theme: bool

    @validator("api_url")
    def validate_api_url(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("message")
    def validate_message(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("lifetime")
    def validate_lifetime(cls, value):
        if value is None or len(value) == 0 or not value.isnumeric():
            raise ValueError("This field must contain an integer.")
        return value

    @validator("event_type")
    def validate_event_type(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value
