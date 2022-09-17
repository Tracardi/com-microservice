from typing import Optional

from app.services.ux.micro_front_end_location import MicroFrontEndLocation
from app.services.ux.rating_popup.configuration import Config
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.notation.dot_template import DotTemplate


async def validate(config: dict, credentials: Optional[dict]) -> Config:
    return Config(**config)


class RatingPopupPlugin(ActionRunner):
    resource: MicroFrontEndLocation
    config: Config

    async def set_up(self, init):
        self.config = Config(**init)
        self.resource = MicroFrontEndLocation(**self.node.microservice.plugin.resource)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        template = DotTemplate()

        message = template.render(self.config.message, dot)

        self.ux.append({
            "tag": "div",
            "props": {
                "class": "tracardi-uix-rating-widget",
                "data-position-vertical": self.config.vertical_position,
                "data-position-horizontal": self.config.horizontal_position,
                "data-title": self.config.title,
                "data-message": message,
                "data-event-type": self.config.event_type,
                "data-api-url": self.config.api_url,
                "data-theme": "dark" if self.config.dark_theme else "",
                "data-auto-hide": self.config.lifetime,
                "data-source-id": self.event.source.id,
                "data-profile-id": self.event.profile.id,
                "data-session-id": self.event.session.id,
                "data-save-event": "yes" if self.config.save_event else "no"
            }
        })
        self.ux.append({"tag": "script", "props": {"src": f"{self.resource.uix_mf_source}/uix/rating_popup/index.js"}})

        return Result(port="response", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='RatingPopupPlugin',
            inputs=["payload"],
            outputs=["response", "error"],
            version='0.7.2',
            license="MIT",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="rating_popup_action",
            init={
                "api_url": "http://localhost:8686",
                "title": None,
                "message": None,
                "lifetime": "6",
                "horizontal_position": "center",
                "vertical_position": "bottom",
                "event_type": None,
                "save_event": True,
                "dark_theme": False
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Plugin configuration",
                        fields=[
                            FormField(
                                id="title",
                                name="Title",
                                description="This text will become a title for your rating popup.",
                                component=FormComponent(type="text", props={"label": "Title"})
                            ),
                            FormField(
                                id="message",
                                name="Popup message",
                                description="That's the message to be displayed in the rating popup. You can use a "
                                            "template here.",
                                component=FormComponent(type="textarea", props={"label": "Message"})
                            ),
                            FormField(
                                id="lifetime",
                                name="Popup lifetime",
                                description="Please provide a number of seconds for the rating popup to be displayed.",
                                component=FormComponent(type="text", props={"label": "Lifetime"})
                            ),
                        ]
                    ),
                    FormGroup(
                        name="Positioning and Styling",
                        fields=[
                            FormField(
                                id="horizontal_position",
                                name="Horizontal position",
                                description="That's the horizontal position of your popup.",
                                component=FormComponent(type="select", props={"label": "Horizontal position", "items": {
                                    "left": "Left",
                                    "center": "Center",
                                    "right": "Right"
                                }})
                            ),
                            FormField(
                                id="vertical_position",
                                name="Vertical position",
                                description="That's the vertical position of your popup.",
                                component=FormComponent(type="select", props={"label": "Vertical position", "items": {
                                    "top": "Top",
                                    "bottom": "Bottom"
                                }})
                            ),
                            FormField(
                                id="dark_theme",
                                name="Dark theme",
                                description="You can switch to dark mode for your popup. Default theme is bright.",
                                component=FormComponent(type="bool", props={"label": "Dark mode"})
                            )
                        ]
                    ),
                    FormGroup(
                        name="Reporting rating",
                        fields=[
                            FormField(
                                id="api_url",
                                name="API URL",
                                description="Provide a URL of Tracardi instance to send event with rating.",
                                component=FormComponent(type="text", props={"label": "API URL"})
                            ),
                            FormField(
                                id="event_type",
                                name="Event type",
                                description="Please provide a type of event to be sent back after selecting rating.",
                                component=FormComponent(type="text", props={"label": "Event type"})
                            ),
                            FormField(
                                id="save_event",
                                name="Save event",
                                description="Please determine whether sent event should be saved or not.",
                                component=FormComponent(type="bool", props={"label": "Save event"})
                            ),
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Rating widget',
            desc='Shows rating widget with defined title and content.',
            icon='react',
            group=["UIX Widgets"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "payload": PortDoc(desc="This port returns given payload without any changes.")
                }
            ),
            frontend=True
        )
    )
