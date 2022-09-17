from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    title: str = ""
    message: str = ""
    cta_button: str = ""
    cta_link: str = ""
    cancel_button: str = ""
    border_radius: int = 2
    border_shadow: int = 1
    min_width: int = 300
    max_width: int = 500,
    hide_after: int = 6000
    position_x: str = "right"
    position_y: str = "bottom"

    @validator("message")
    def should_no_be_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Message should not be empty")
        return value

    @validator("cta_button")
    def cta_no_be_empty(cls, value):
        if len(value) == 0:
            raise ValueError("CTA should not be empty")
        return value
