from typing import Optional

from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from .config import Config
from ..credentials import TrelloCredentials
from tracardi.process_engine.action.v1.connectors.trello.trello_client import TrelloClient
from ..trello_plugin import TrelloPlugin


async def validate(config: dict, credentials: Optional[dict]) -> Config:
    credentials = TrelloCredentials(**credentials)
    plugin_config = Config(**config)
    client = TrelloClient(credentials.api_key, credentials.token)
    list_id = await client.get_list_id(plugin_config.board_url, plugin_config.list_name)
    plugin_config = Config(**plugin_config.dict(exclude={"list_id"}), list_id=list_id)
    return plugin_config


class TrelloMemberAdder(TrelloPlugin):
    config: Config

    async def set_up(self, init):
        self.config = Config(**init)
        self.set_up_trello(self.node)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        member_id = dot[self.config.member_id]
        card_name = dot[self.config.card_name]

        try:
            result = await self._client.add_member(self.config.list_id, card_name, member_id)
        except (ConnectionError, ValueError) as e:
            self.console.error(str(e))
            return Result(port="error", value=payload)

        return Result(port="response", value=result)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='plugins.trello.add_member.plugin',
            className='TrelloMemberAdder',
            inputs=["payload"],
            outputs=["response", "error"],
            version='0.7.2',
            license="MIT",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="trello/add_trello_member_action",
            init={
                "board_url": None,
                "card_name": None,
                "list_name": None,
                "member_id": None
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Trello Add Member Configuration",
                        fields=[
                            FormField(
                                id="board_url",
                                name="URL of Trello board",
                                description="Please provide the URL of your board.",
                                component=FormComponent(type="text", props={"label": "Board URL"})
                            ),
                            FormField(
                                id="list_name",
                                name="Name of Trello list",
                                description="Please provide the name of your Trello list.",
                                component=FormComponent(type="text", props={"label": "List name"})
                            ),
                            FormField(
                                id="card_name",
                                name="Name of your card",
                                description="Please provide path to the name of the card that you want to add member "
                                            "to.",
                                component=FormComponent(type="dotPath",
                                                        props={"label": "Card name", "defaultMode": "2"})
                            ),
                            FormField(
                                id="member_id",
                                name="ID of the member",
                                description="Please provide the path to the field containing ID of the member that you "
                                            "want to add.",
                                component=FormComponent(type="dotPath",
                                                        props={"label": "ID of the member", "defaultMode": "2"})
                            )
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Add Trello Member',
            desc='Adds a member to given card on given list in Trello.',
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
