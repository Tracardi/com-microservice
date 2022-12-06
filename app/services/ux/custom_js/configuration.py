from json import JSONDecodeError

import json
from typing import Optional
from tracardi.service.plugin.domain.config import PluginConfig
from pydantic import validator


class Config(PluginConfig):
    content: Optional[str] = ""
    attributes: Optional[str] = "{}"

    @validator("attributes")
    def validate_file_path(cls, value):
        try:
            json.loads(value)
            return value
        except JSONDecodeError:
            raise ValueError("Could not parse invalid JSON object.")
