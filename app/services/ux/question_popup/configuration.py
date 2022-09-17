from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    api_url: str
    popup_title: str
    content: str
    left_button_text: str
    right_button_text: str
    horizontal_pos: str
    vertical_pos: str
    event_type: str
    save_event: bool
    popup_lifetime: str
    dark_theme: bool

    @validator("popup_lifetime")
    def validate_popup_lifetime(cls, value):
        if value is None or len(value) == 0 or not value.isnumeric():
            raise ValueError("This field must contain an integer.")
        return value

    @validator("api_url")
    def validate_api_url(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("left_button_text")
    def validate_left_button_text(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("right_button_text")
    def validate_right_button_text(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value

    @validator("event_type")
    def validate_event_type(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("This field cannot be empty.")
        return value
