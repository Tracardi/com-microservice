import os
from decouple import config, UndefinedValueError

from tracardi.exceptions.log_handler import get_logger

logger = get_logger(__name__)


class MicroserviceConfig:
    def __init__(self, env):
        try:
            self.api_key = config('API_KEY')
        except UndefinedValueError as e:
            logger.error(f"API_KEY environment variable not defined. {str(e)}")
            exit(1)


microservice = MicroserviceConfig(os.environ)
