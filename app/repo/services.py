from app.services.trello.credentials import TrelloCredentials
from app.services.ux.micro_front_end_location import MicroFrontEndLocation
from tracardi.service.plugin.domain.register import FormField, FormGroup, Form, FormComponent, Plugin, Spec, MetaData, \
    Documentation, PortDoc

from app.repo.domain import ServiceConfig, ServiceResource, ServicesRepo, PluginConfig
from app.services import trello, ux

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
                    tags=['microservice', 'remote'],
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
        ),
        "597da587-f25a-49ba-9f95-f3424dd3b159": ServiceConfig(
            name="UIX Widgets",
            resource=ServiceResource(
                form=Form(groups=[
                    FormGroup(
                        name="UIX resource configuration",
                        fields=[
                            FormField(
                                id="uix_mf_source",
                                name="Micro-front-end source location",
                                description="This service needs to download micro-front-end code. Please provide the "
                                            "location of the micro-front-end javascript code. Usually it is the "
                                            "micro-service URL or the CDN that the code was uploaded to.",
                                component=FormComponent(type="text",
                                                        props={"label": "URL"})
                            )
                        ]
                    )]),
                init=MicroFrontEndLocation.create(),
                validator=MicroFrontEndLocation
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
                    name='UIX Widgets Microservice',
                    desc='Microservice that runs Trello plugins.',
                    icon='react',
                    group=["UIX Widgets"],
                    tags=['microservice', 'remote', 'uix'],
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
                ),

            ),

            plugins={
                "3d0828b8-9e17-4ae8-ab0c-d82fd3638b3d": PluginConfig(
                    name="Info pop-up",
                    validator=ux.snackbar.plugin.validate,
                    plugin=ux.snackbar.plugin.SnackBarUx,
                    registry=ux.snackbar.plugin.register()
                ),
                "bb7ecaf8-e3c9-424a-a3bd-df79e006e897": PluginConfig(
                    name="Rating widget",
                    validator=ux.rating_popup.plugin.validate,
                    plugin=ux.rating_popup.plugin.RatingPopupPlugin,
                    registry=ux.rating_popup.plugin.register()
                ),
                "aaaecaf8-efc9-c24b-a34d-df79e003486": PluginConfig(
                    name="Question pop-up",
                    validator=ux.question_popup.plugin.validate,
                    plugin=ux.question_popup.plugin.QuestionPopupPlugin,
                    registry=ux.question_popup.plugin.register()
                ),
                "730e35c1-d973-4672-9630-bad52c8d67ed": PluginConfig(
                    name="CTA message",
                    validator=ux.cta_message.plugin.validate,
                    plugin=ux.cta_message.plugin.CtaMessageUx,
                    registry=ux.cta_message.plugin.register()
                ),
                "4d98e211-7f80-4807-8616-3d9a24570122": PluginConfig(
                    name="Contact form",
                    validator=ux.contact_popup.plugin.validate,
                    plugin=ux.contact_popup.plugin.ContactPopupPlugin,
                    registry=ux.contact_popup.plugin.register()
                )
            }
        ),

    })
