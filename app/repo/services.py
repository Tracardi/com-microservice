from tracardi.process_engine.action.v1.connectors.trello.credentials import TrelloCredentials
from tracardi.service.plugin.domain.register import FormField, FormGroup, Form, FormComponent, Plugin, Spec, MetaData, \
    Documentation, PortDoc

from app.repo.domain import ServiceConfig, ServiceResource, ServicesRepo, PluginConfig
from app.services import trello

repo = ServicesRepo(
    repo={
        "a307b281-2629-4c12-b6e3-df1ec9bca35a": ServiceConfig(
            name="Trello",
            resource=ServiceResource(
                form=Form(groups=[
                    FormGroup(
                        name="Service connection configuration",
                        description="This service needs to connect to Trello. Please provide API credentials.",
                        fields=[
                            FormField(
                                id="api_key",
                                name="Trello API KEY",
                                description="Please Provide Trello API KEY.",
                                component=FormComponent(type="text",
                                                        props={"label": "API KEY"})
                            ),
                            FormField(
                                id="token",
                                name="Trello TOKEN",
                                description="Please Provide Trello TOKEN.",
                                component=FormComponent(type="text",
                                                        props={"label": "TOKEN"})
                            )
                        ]
                    )]),
                init=TrelloCredentials.create(),
                validator=TrelloCredentials
            ),
            microservice=Plugin(
                start=False,
                spec=Spec(
                    module='tracardi.process_engine.action.v1.microservice.plugin',
                    className='MicroserviceAction',
                    inputs=["payload"],
                    outputs=["response", "error"],
                    version='0.7.2',
                    license="MIT",
                    author="Risto Kowaczewski"
                ),
                metadata=MetaData(
                    name='Trello Microservice',
                    desc='Microservice that runs Trello plugins.',
                    icon='trello',
                    group=["Connectors"],
                    remote=True,
                    documentation=Documentation(
                        inputs={
                            "payload": PortDoc(desc="This port takes payload object.")
                        },
                        outputs={
                            "response": PortDoc(desc="This port returns microservice response."),
                            "error": PortDoc(desc="This port returns microservice error.")
                        }
                    )
                )),
            plugins={
                "a04381af-c008-4328-ab61-0e73825903ce": PluginConfig(
                    name="Add card",
                    validator=trello.add_card.plugin.validate,
                    plugin=trello.add_card.plugin.TrelloCardAdder,
                    registry=trello.add_card.plugin.register()
                ),
                "9062083f-6bb5-4208-ae31-c2562161ab9b": PluginConfig(
                    name="Move card",
                    validator=trello.move_card.plugin.validate,
                    plugin=trello.move_card.plugin.TrelloCardMover,
                    registry=trello.move_card.plugin.register()
                ),
                "b5a5ad32-95a8-4a50-bd36-d29f3e98c523": PluginConfig(
                    name="Delete card",
                    validator=trello.delete_card.plugin.validate,
                    plugin=trello.delete_card.plugin.TrelloCardRemover,
                    registry=trello.delete_card.plugin.register()
                ),
                "0c52a414-8fc6-40ff-b3c7-27183285c753": PluginConfig(
                    name="Add Member",
                    validator=trello.add_member.plugin.validate,
                    plugin=trello.add_member.plugin.TrelloMemberAdder,
                    registry=trello.add_member.plugin.register()
                ),
            }
        )
    })
