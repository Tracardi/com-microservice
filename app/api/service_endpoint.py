import json
from json import JSONDecodeError
from typing import Union, Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError, BaseModel
from starlette.responses import JSONResponse

from app.api.auth.auth_bearer import JWTBearer
from tracardi.service.module_loader import import_package, load_callable, is_coroutine
from tracardi.service.plugin.domain.console import Console
from tracardi.service.plugin.domain.register import Plugin

from tracardi.service.plugin.service import plugin_context

from app.repo.domain import PluginExecContext, ServiceResource
from app.repo.services import repo
from app.utils.converter import convert_errors

router = APIRouter()


@router.post("/plugin/{module}/{endpoint_function}", dependencies=[Depends(JWTBearer())], tags=["microservice"],
             response_model=dict)
async def get_data_for_plugin(module: str, endpoint_function: str, request: Request):
    """
    Calls helper method from Endpoint class in plugin's module
    """

    try:
        if not module.startswith('app.services'):
            raise HTTPException(status_code=404, detail="This is not helper endpoint.")

        module = import_package(module)
        endpoint_module = load_callable(module, 'Endpoint')
        function_to_call = getattr(endpoint_module, endpoint_function)

        try:
            body = await request.json()
        except JSONDecodeError:
            body = {}

        if is_coroutine(function_to_call):
            return await function_to_call(body)
        return function_to_call(body)

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/services", dependencies=[Depends(JWTBearer())], tags=["microservice"], response_model=dict)
async def get_all_services():
    services = list(repo.get_all_services())
    return {
        "total": len(services),
        "result": {id: name for id, name in services}
    }


@router.get("/actions", dependencies=[Depends(JWTBearer())], tags=["microservice"], response_model=dict)
async def get_actions(service_id: str):
    actions = list(repo.get_all_action_plugins(service_id))
    return {
        "total": len(actions),
        "result": {id: name for id, name in actions}
    }


@router.get("/plugin/form", dependencies=[Depends(JWTBearer())], tags=["microservice"], response_model=dict)
async def get_plugin_form(service_id: str, action_id: str):
    init, form = repo.get_plugin_form_an_init(service_id, action_id)

    return {
        "init": init if init is not None else {},
        "form": form.dict() if form is not None else None
    }


@router.get("/service/resource", dependencies=[Depends(JWTBearer())], tags=["microservice"],
            response_model=Union[dict, None])
async def get_service_resource(service_id: str):

    """
    Returns service resource definition.
    :param service_id: str
    :return: Union[dict, None]
    """

    service = repo.get_service(service_id)
    if service is not None and isinstance(service.resource, BaseModel):
        return service.resource.dict(exclude={"validator": ...})
    return None


@router.post("/service/resource/validate", dependencies=[Depends(JWTBearer())], tags=["microservice"])
async def validate_resource(service_id: str, resource: dict):
    """
    Returns service resource definition.
    :param resource: dict
    :param service_id: str
    :return: Union[dict, None]
    """

    if service_id == '':
        raise ValueError("Empty param service_id")

    service = repo.get_service(service_id)
    if service is None or not isinstance(service.resource, ServiceResource):
        raise RuntimeError('Service resource validator not defined.')

    try:
        service.resource.validator(**resource)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )

    return True


@router.get("/plugin/registry", dependencies=[Depends(JWTBearer())], tags=["microservice"],
            response_model=Union[Plugin, None])
async def get_plugin_registry(service_id: str):

    """
    Returns plugin specification

    :param service_id:
    :return: Union[Plugin, None]
    """

    return repo.get_plugin_registry(service_id)


@router.post("/plugin/validate", dependencies=[Depends(JWTBearer())], tags=["microservice"])
async def validate_plugin_configuration(service_id: str, action_id: str, config: Optional[dict]=None, credentials: dict = None):
    try:
        validator = repo.get_plugin_validator(service_id, action_id)
        return await validator(config, credentials)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )


@router.post("/plugin/run", dependencies=[Depends(JWTBearer())], tags=["microservice"])
async def run_plugin(service_id: str, action_id: str, data: PluginExecContext):

    # """
    # Runs the plugin.
    # :param service_id:
    # :param action_id:
    # :param data:
    # :return:
    # """
    #
    # try:
        plugin_type = repo.get_plugin(service_id, action_id)
        if plugin_type:
            plugin = plugin_type()
            plugin.console = Console(plugin_type, __name__)
            # set context
            data.context['node']['className'] = plugin_type.__name__
            data.context['node']['module'] = __name__

            plugin_context.set_context(plugin, data.context, include=['node'])

            await plugin.set_up(data.init)
            result = await plugin.run(**data.params)
            return {
                "result": result,
                "context": plugin_context.get_context(plugin, include=['node']),
                "console": plugin.console.dict()
            }
        return {}
    # except ValidationError as e:
    #     return JSONResponse(
    #         status_code=422,
    #         content=jsonable_encoder(convert_errors(e))
    #     )
