import os
from decouple import config


class MicroserviceConfig:
    def __init__(self, env):
        self.api_key = config('API_KEY')


microservice = MicroserviceConfig(os.environ)
