from typing import Optional, Union

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from starlette.responses import JSONResponse

from tracardi.service.plugin.domain.register import Plugin

from tracardi.service.plugin.service import plugin_context

from app.repo.domain import PluginExecContext
from app.repo.services import repo
from app.utils.converter import convert_errors

router = APIRouter()


@router.get("/services", tags=["microservice"], response_model=dict)
async def get_all_services():
    services = list(repo.get_all_services())
    return {
        "total": len(services),
        "result": {id: name for id, name in services}
    }


@router.get("/actions", tags=["microservice"], response_model=dict)
async def get_actions(service_id: str):
    actions = list(repo.get_all_action_plugins(service_id))
    return {
        "total": len(actions),
        "result": {id: name for id, name in actions}
    }


@router.get("/plugin/form", tags=["microservice"], response_model=dict)
async def get_plugin(service_id: str, action_id: str):
    init, form = repo.get_plugin_form_an_init(service_id, action_id)

    return {
        "init": init if init is not None else {},
        "form": form.dict() if form is not None else None
    }


@router.get("/service/resource", tags=["microservice"], response_model=Union[dict, None])
async def get_plugin_registry(service_id: str):
    service = repo.get_service(service_id)
    if service is not None:
        return service.resource.dict(exclude={"validator": ...})
    return None


@router.get("/plugin/registry", tags=["microservice"], response_model=Union[Plugin, None])
async def get_plugin_registry(service_id: str):
    return repo.get_plugin_registry(service_id)


@router.post("/plugin/validate", tags=["microservice"], response_model=dict)
async def validate_plugin_configuration(service_id: str, action_id: str, data: dict):
    try:
        validator = repo.get_plugin_validator(service_id, action_id)
        return validator(**data)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )


@router.post("/plugin/run", tags=["microservice"], response_model=dict)
async def run_plugin(service_id: str, action_id: str, data: PluginExecContext):
    try:
        plugin_type = repo.get_plugin(service_id, action_id)
        print(data.init)
        if plugin_type:
            plugin = plugin_type()
            # set context
            data.context['node']['className'] = plugin_type.__name__
            data.context['node']['module'] = __name__
            plugin_context.set_context(plugin, data.context, include=['node'])
            print("context", data.context['node'])
            print("init", data.init)
            await plugin.set_up(data.init)
            print(await plugin.run(**data.params))
        return {}
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
