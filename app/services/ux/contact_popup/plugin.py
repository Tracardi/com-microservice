from typing import Optional
from uuid import uuid4

from app.services.ux.contact_popup.configuration import Config
from app.services.ux.micro_front_end_location import MicroFrontEndLocation
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.notation.dot_template import DotTemplate


async def validate(config: dict, credentials: Optional[dict]) -> Config:
    return Config(**config)


class ContactPopupPlugin(ActionRunner):
    resource: MicroFrontEndLocation
    config: Config

    async def set_up(self, init):
        self.config = Config(**init)
        self.resource = MicroFrontEndLocation(**self.node.microservice.plugin.resource)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        template = DotTemplate()

        content = template.render(self.config.content, dot)

        self.ux.append({
            "tag": "link",
            "props": {
                "rel": "stylesheet",
                "href": f"{self.resource.uix_mf_source}/uix/contact-popup/index.css"
            }
        })
        self.ux.append({
            "tag": "div",
            "props": {
                "class": "tracardi-uix-contact-widget",
                "data-message": content,
                "data-contact-type": self.config.contact_type,
                "data-api-url": self.config.api_url,
                "data-source-id": self.event.source.id,
                "data-profile-id": self.event.profile.id,
                "data-session-id": self.session.id if self.session is not None else str(uuid4()),
                "data-event-type": self.config.event_type,
                "data-theme": "dark" if self.config.dark_theme else "",
                "data-position-horizontal": self.config.horizontal_pos,
                "data-position-vertical": self.config.vertical_pos,
                "data-save-event": "yes" if self.config.save_event else "no"
            }
        })
        self.ux.append({
            "tag": "script",
            "props": {"src": f"{self.resource.uix_mf_source}/uix/contact-popup/index.js"}
        })

        return Result(port="response", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='ContactPopupPlugin',
            inputs=["payload"],
            outputs=["response", "error"],
            version='0.7.2',
            license="MIT",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="contact_popup_action",
            init={
                "api_url": "http://localhost:8686",
                "content": None,
                "contact_type": "email",
                "horizontal_pos": "center",
                "vertical_pos": "bottom",
                "event_type": None,
                "save_event": True,
                "dark_theme": False
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Contact form configuration",
                        fields=[
                            FormField(
                                id="content",
                                name="Popup message",
                                description="That's the message to be displayed in the popup. You can use a template "
                                            "here.",
                                component=FormComponent(type="textarea", props={"label": "Message"})
                            ),
                            FormField(
                                id="contact_type",
                                name="Contact data type",
                                description="Please select type of the contact data to be provided by user.",
                                component=FormComponent(type="select", props={"label": "Contact", "items": {
                                    "email": "Email",
                                    "phone": "Phone number"
                                }})
                            ),
                        ]
                    ),
                    FormGroup(
                        name="Positioning and Styling",
                        fields=[
                            FormField(
                                id="horizontal_pos",
                                name="Horizontal position",
                                description="That's the horizontal position of your popup.",
                                component=FormComponent(type="select", props={"label": "Horizontal position", "items": {
                                    "left": "Left",
                                    "center": "Center",
                                    "right": "Right"
                                }})
                            ),
                            FormField(
                                id="vertical_pos",
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
                        name="Event configuration",
                        description="When the user fills the form an event with its content will be sent back to "
                                    "Tracardi.",
                        fields=[
                            FormField(
                                id="api_url",
                                name="API URL",
                                description="Provide a URL of Tracardi instance to send event with contact "
                                            "information.",
                                component=FormComponent(type="text", props={"label": "API URL"})
                            ),
                            FormField(
                                id="event_type",
                                name="Event type",
                                description="Please provide a type of event to be sent back after submitting contact "
                                            "data by the user.",
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
            name='Contact form',
            desc='Shows a popup with field for contact data to user, according to configuration.',
            icon='react',
            group=["UIX Widgets"],
            frontend=True
        )
    )
