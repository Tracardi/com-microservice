from typing import Optional
from uuid import uuid4

from app.services.ux.micro_front_end_location import MicroFrontEndLocation
from app.services.ux.question_popup.configuration import Config
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.notation.dot_template import DotTemplate


async def validate(config: dict, credentials: Optional[dict]) -> Config:
    return Config(**config)


class QuestionPopupPlugin(ActionRunner):
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
            "tag": "div",
            "props": {
                "class": "tracardi-question-widget",
                "data-api-url": self.config.api_url,
                "data-source-id": self.event.source.id,
                "data-session-id": self.session.id if self.session is not None else str(uuid4()),
                "data-left-button-text": self.config.left_button_text,
                "data-right-button-text": self.config.right_button_text,
                "data-popup-title": self.config.popup_title,
                "data-content": content,
                "data-horizontal-position": self.config.horizontal_pos,
                "data-vertical-position": self.config.vertical_pos,
                "data-popup-lifetime": self.config.popup_lifetime,
                "data-bg-color": self.config.styling.color.background,
                "data-event-type": self.config.event_type,
                "data-text-color": self.config.styling.color.text,
                "data-border-width": self.config.styling.border.size,
                "data-border-radius": self.config.styling.border.radius,
                "data-border-color": self.config.styling.border.color,
                "data-padding-left": self.config.styling.padding.left,
                "data-padding-right": self.config.styling.padding.right,
                "data-padding-top": self.config.styling.padding.top,
                "data-padding-bottom": self.config.styling.padding.bottom,
                "data-margin-left": self.config.styling.margin.left,
                "data-margin-right": self.config.styling.margin.right,
                "data-margin-top": self.config.styling.margin.top,
                "data-margin-bottom": self.config.styling.margin.bottom,
                "data-save-event": "yes" if self.config.save_event else "no",
                "data-profile-id": self.event.profile.id
            }
        })
        self.ux.append({
            "tag": "script",
            "props": {"src": f"{self.resource.uix_mf_source}/uix/question-popup/index.js"}
        })

        return Result(port="response", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='QuestionPopupPlugin',
            inputs=["payload"],
            outputs=["response", "error"],
            version='0.7.2',
            license="MIT",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="question_popup_action",
            init={
                "api_url": "http://localhost:8686",
                "popup_title": "",
                "content": "",
                "left_button_text": None,
                "right_button_text": None,
                "horizontal_pos": "center",
                "vertical_pos": "bottom",
                "event_type": None,
                "save_event": True,
                "popup_lifetime": "6",
                "styling": {
                    "margin": {
                        "left": 0, "top": 0, "right": 0, "bottom": 0
                    },
                    "padding": {
                        "left": 0, "top": 0, "right": 0, "bottom": 0
                    },
                    "color": {
                        "background": "rgba(229,229,229,0.9)",
                        "text": "rgba(0,0,0,1)"
                    },
                    "border": {
                        "size": 0,
                        "radius": 0,
                        "color": "black"
                    }
                }
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Pop-up configuration",
                        fields=[
                            FormField(
                                id="popup_title",
                                name="Popup title",
                                description="This text will become a title for your popup.",
                                component=FormComponent(type="text", props={"label": "Title"})
                            ),
                            FormField(
                                id="content",
                                name="Popup content",
                                description="That's the message to be displayed in the popup. You can use a template "
                                            "here.",
                                component=FormComponent(type="textarea", props={"label": "Message"})
                            ),
                            FormField(
                                id="popup_lifetime",
                                name="Popup lifetime",
                                description="Please provide a number of seconds for the popup to be displayed.",
                                component=FormComponent(type="text", props={"label": "Lifetime"})
                            ),
                        ]
                    ),
                    FormGroup(
                        name="Button text",
                        fields=[
                            FormField(
                                id="left_button_text",
                                name="Left button text",
                                description="That's the text to be displayed on the left button. It will be sent back "
                                            "in event properties if left button gets clicked.",
                                component=FormComponent(type="text", props={"label": "Left button"})
                            ),
                            FormField(
                                id="right_button_text",
                                name="Right button text",
                                description="That's the text to be displayed on the right button. It will be sent back "
                                            "in event properties if right button gets clicked.",
                                component=FormComponent(type="text", props={"label": "Right button"})
                            ),
                            ]
                    ),
                    FormGroup(
                        name="Positioning",
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
                            ]
                    ),
                    FormGroup(
                        name="Styling",
                        fields=[
                            FormField(
                                id="styling",
                                name="Pop-up styling",
                                component=FormComponent(type="boxStyling")
                            )
                        ]
                    ),
                    FormGroup(
                        name="Event configuration",
                        description="When the user answers the question an event will be sent back to Tracardi.",
                        fields=[
                            FormField(
                                id="api_url",
                                name="API URL",
                                description="Provide a URL of Tracardi instance to send event with answer.",
                                component=FormComponent(type="text", props={"label": "API URL"})
                            ),
                            FormField(
                                id="event_type",
                                name="Event type",
                                description="Please provide a type of event to be sent back.",
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
            name='Question popup',
            desc='Shows question popup to user, according to configuration.',
            icon='react',
            group=["UIX Widgets"],
            frontend=True
        )
    )
