from typing import Optional

from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from .config import Config
from ..credentials import TrelloCredentials
from ..trello_client import TrelloClient
from ..trello_plugin import TrelloPlugin


async def validate(config: dict, credentials: Optional[dict]) -> Config:
    credentials = TrelloCredentials(**credentials)
    plugin_config = Config(**config)
    client = TrelloClient(credentials.api_key, credentials.token)
    list_id1 = await client.get_list_id(plugin_config.board_url, plugin_config.list_name1)
    list_id2 = await client.get_list_id(plugin_config.board_url, plugin_config.list_name2)
    plugin_config = Config(**plugin_config.dict(exclude={"list_id1", "list_id2"}), list_id1=list_id1, list_id2=list_id2)
    return plugin_config


class TrelloCardMover(TrelloPlugin):
    config: Config

    async def set_up(self, init):
        self.config = Config(**init)
        self.set_up_trello(self.node)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        card_name = dot[self.config.card_name]

        try:
            result = await self._client.move_card(self.config.list_id1, self.config.list_id2, card_name)
        except (ConnectionError, ValueError) as e:
            self.console.error(str(e))
            return Result(port="error", value={"message": str(e)})

        return Result(port="response", value=result)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='plugins.trello.move_card.plugin',
            className='TrelloCardMover',
            inputs=["payload"],
            outputs=["response", "error"],
            version='0.7.2',
            license="MIT",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="trello/move_trello_card_action",
            init={
                "board_url": None,
                "list_name1": None,
                "list_name2": None,
                "card_name": None
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Trello Move Card Configuration",
                        fields=[
                            FormField(
                                id="board_url",
                                name="URL of Trello board",
                                description="Please provide the URL of your board.",
                                component=FormComponent(type="text", props={"label": "Board URL"})
                            ),
                            FormField(
                                id="list_name1",
                                name="Name of current Trello list",
                                description="Please provide the name of your Trello list that card is currently on.",
                                component=FormComponent(type="text", props={"label": "List name"})
                            ),
                            FormField(
                                id="list_name2",
                                name="Name of target Trello list",
                                description="Please provide the name of your Trello list that you want to move your "
                                            "card to.",
                                component=FormComponent(type="text", props={"label": "List name"})
                            ),
                            FormField(
                                id="card_name",
                                name="Name of your card",
                                description="Please provide path to the name of the card that you want to move.",
                                component=FormComponent(type="dotPath",
                                                        props={"label": "Card name", "defaultMode": "2"})
                            )
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Move Trello Card',
            desc='Moves card from given list on given board to another list on that board in Trello.',
            icon='trello',
            group=["Trello"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "response": PortDoc(desc="This port returns a response from Trello API."),
                    "error": PortDoc(desc="This port gets triggered if an error occurs.")
                }
            )
        )
    )
