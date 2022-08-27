from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.storage.driver import storage

from app.services.trello.credentials import TrelloCredentials
from app.services.trello.trello_client import TrelloClient
from tracardi.service.wf.domain.node import Node


class TrelloPlugin(ActionRunner):
    _client: TrelloClient

    def set_up_trello(self, node: Node):
        credentials = TrelloCredentials(**node.microservice.plugin.resource)
        client = TrelloClient(credentials.api_key, credentials.token)

        self._client = client
        self._client.set_retries(self.node.on_connection_error_repeat)
