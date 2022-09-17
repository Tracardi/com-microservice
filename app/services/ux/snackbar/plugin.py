from typing import Optional
from app.services.ux.micro_front_end_location import MicroFrontEndLocation
from app.services.ux.snackbar.configuration import Configuration
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.notation.dot_template import DotTemplate


async def validate(config: dict, credentials: Optional[dict]) -> Configuration:
    return Configuration(**config)


class SnackBarUx(ActionRunner):
    resource: MicroFrontEndLocation
    config: Configuration

    async def set_up(self, init):
        self.config = Configuration(**init)
        self.resource = MicroFrontEndLocation(**self.node.microservice.plugin.resource)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        template = DotTemplate()

        message = template.render(self.config.message, dot)

        self.ux.append({
            "tag": "div",
            "props": {
                "class": "tracardi-uix-snackbar",
                "data-type": self.config.type,
                "data-message": message,
                "data-vertical": self.config.position_y,
                "data-horizontal": self.config.position_x,
                "data-auto-hide": self.config.hide_after
            }
        })
        self.ux.append({"tag": "script", "props": {"src": f"{self.resource.uix_mf_source}/uix/snackbar/index.js"}})

        return Result(port="response", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='SnackBarUx',
            inputs=["payload"],
            outputs=["response", "error"],
            init={
                "type": "success",
                "message": "",
                "hide_after": 6000,
                "position_x": "center",
                "position_y": "bottom"
            },
            version='0.7.2',
            license="MIT",
            author="Risto Kowaczewski",
            form=Form(
                groups=[
                    FormGroup(
                        name="Widget Message Configuration",
                        fields=[
                            FormField(
                                id="message",
                                name="Pop-up message",
                                description="Provide message that will be shown on the web page.",
                                component=FormComponent(type="textarea", props={"label": "message"})
                            ),
                            FormField(
                                id="type",
                                name="Alert type",
                                description="Select alert type.",
                                component=FormComponent(type="select", props={"label": "Alert type", "items": {
                                    "error": "Error",
                                    "warning": "Warning",
                                    "success": "Success",
                                    "info": "Info"
                                }})
                            ),
                            FormField(
                                id="hide_after",
                                name="Hide message after",
                                description="Type number of milliseconds the message must be visible. Default: 6000. 6sec.",
                                component=FormComponent(type="text", props={"label": "hide after"})
                            ),
                            FormField(
                                id="position_y",
                                name="Vertical position",
                                description="Select where would you like to place the message.",
                                component=FormComponent(type="select", props={"label": "Vertical position", "items": {
                                    "bottom": "Bottom",
                                    "top": "Top"
                                }})
                            ),
                            FormField(
                                id="position_x",
                                name="Horizontal position",
                                description="Select where would you like to place the message.",
                                component=FormComponent(type="select", props={"label": "Horizontal position", "items": {
                                    "left": "Left",
                                    "center": "Center",
                                    "right": "Right"
                                }})
                            ),
                        ])
                ]),

        ),
        metadata=MetaData(
            name='Show snack bar',
            desc='Shows snack bar pop-up on the front end.',
            icon='react',
            group=["UIX Widgets"],
            frontend=True
        )
    )
