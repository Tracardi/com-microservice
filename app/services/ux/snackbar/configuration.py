from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    type: str = "success"
    message: str
    hide_after: str
    position_x: str
    position_y: str

    @validator("message")
    def should_no_be_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Message should not be empty")
        return value

    @validator("hide_after")
    def hide_after_should_be_numeric(cls, value: str):
        if not value.isnumeric():
            raise ValueError("This value should be numeric")
        return value
