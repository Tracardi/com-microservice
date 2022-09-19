from pydantic import validator

from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    uix_source: str
    props: dict

    @validator("uix_source")
    def validate_file_path(cls, value):
        if isinstance(value, str) and not value.endswith(".js"):
            raise ValueError("Widget file has to be .js file.")
        return value
