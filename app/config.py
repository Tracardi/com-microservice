import logging

import os
from decouple import config, UndefinedValueError


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MicroserviceConfig:
    def __init__(self, env):
        try:
            self.api_key = config('API_KEY')
        except UndefinedValueError as e:
            logger.error(f"API_KEY environment variable not defined. {str(e)}")
            exit(1)


microservice = MicroserviceConfig(os.environ)
