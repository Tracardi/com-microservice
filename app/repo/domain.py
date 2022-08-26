from typing import Type, Dict, Tuple, Optional
from pydantic import BaseModel
from tracardi.service.plugin.domain.register import Form, Plugin
from tracardi.service.plugin.runner import ActionRunner


class PluginExecContext(BaseModel):
    context: dict
    params: dict
    init: dict


class PluginConfig(BaseModel):
    name: str
    validator: Type[BaseModel]
    plugin: Type[ActionRunner]
    registry: Plugin


class ServiceResource(BaseModel):
    form: Form
    init: BaseModel
    validator: Type[BaseModel]


class ServiceConfig(BaseModel):
    name: str
    microservice: Plugin  # ? registry
    plugins: Dict[str, PluginConfig]
    resource: Optional[ServiceResource] = None


class ServicesRepo(BaseModel):
    repo: Dict[str, ServiceConfig]

    def get_all_services(self) -> Tuple[str, str]:
        for id, service in self.repo.items():
            yield id, service.name

    def get_all_action_plugins(self, service_id: str) -> Tuple[str, str]:
        if service_id in self.repo:
            service = self.repo[service_id]
            for id, plugin_config in service.plugins.items():
                yield id, plugin_config.name

    def get_service(self, service_id: str) -> Optional[ServiceConfig]:
        if service_id in self.repo:
            return self.repo[service_id]
        return None

    def get_plugin(self, service_id: str, plugin_id: str) -> Optional[Type[ActionRunner]]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.plugin
        return None

    def get_plugin_registry(self, service_id: str) -> Optional[Plugin]:
        if service_id in self.repo:
            service = self.repo[service_id]
            return service.microservice
        return None

    def get_plugin_form_an_init(self, service_id: str, plugin_id: str) -> Tuple[Optional[dict], Optional[Form]]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.registry.spec.init, plugin_config.registry.spec.form
        return None, None

    def get_plugin_validator(self, service_id: str, plugin_id: str) -> Type[BaseModel]:
        if service_id in self.repo:
            service = self.repo[service_id]
            if plugin_id in service.plugins:
                plugin_config = service.plugins[plugin_id]
                return plugin_config.validator
        raise LookupError(f"Missing validator configuration for service {service_id} and plugin {plugin_id}")
