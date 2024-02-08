Run microservice

```bash
docker run -p 20000:20000 -e SECRET=c1d44724c7543f19dc834d8bd8c86a92 -e API_KEY=983d32f6-4cd1-4ec1-b20c-f99f3eb8277b-db3e32536f658b6960aaad407c1a169cd02d7fd3 tracardi/com-microservice:0.9.0-dev
```

# Moving a plugin to a microservice

You have to go through the following steps.

## Changes to the plugin code

1. Copy the plugin to `app/services` folder.
2. Add it to `__init.py__` like this:

```python
from .chats.livechat.plugin import LivechatWidgetPlugin
```

3. Change the validate function to have to following signature:

```python
async def validate(config: dict, credentials: Optional[dict]):
    ...
```

Remember to set async.

4. Change the `set_up` method so validation is through config object not validate function:

```Python
self.config = Config(**init)
```

5. Change to output of the plugin to have 2 ports:

```python
outputs = ["response", "error"],  # Plugin.Spec.outputs
```

6. Return data on response or error port.

## Plugin registration

1. Create a new service and add the following code to `app/repo/services.py` (optionally you can skip this if the service is created and you would like only to extend its
   actions)

```python
"a307b281-2629-4c12-b6e3-df1ec9bca35a": ServiceConfig(
    name="Trello",
    resource=ServiceResource(
        form=Form(groups=[
            # Required service properties
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
        # Object for microservice credentials
        init=TrelloCredentials.create(),
        validator=TrelloCredentials
    ),
    microservice=Plugin(
        start=False,
        spec=Spec(
            module='tracardi.process_engine.action.v1.microservice.plugin',
            className='MicroserviceAction',
            inputs=["payload"],
            # Remember about the outputs
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
            # It must be remote
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
        # To be filled, see below
    }
),
```

2. Fill microservice actions in `ServiceConfig.plugins`. Section `To be filled, see below` in the above code.
```python
plugins={
    "a04381af-c008-4328-ab61-0e73825903ce": PluginConfig(
        # This is the name of the service
        name="Add card",
        # Validator that points to validate function
        validator=trello.add_card.plugin.validate,
        # Plugin class
        plugin=trello.add_card.plugin.TrelloCardAdder,
        # Registry method
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
```
   