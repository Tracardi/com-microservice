import logging
import os
from time import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from app import config
from app.api import service_endpoint, auth_endpoint
from tracardi.config import tracardi

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_local_dir = os.path.dirname(__file__)

print(f"TRACARDI version {str(tracardi.version)}")
if len(config.microservice.api_key) < 32:
    raise EnvironmentError("API_KEY must be at least 32 chars long")

application = FastAPI(
    title="Tracardi Microservices",
    version=str(tracardi.version),
    contact={
        "name": "Risto Kowaczewski",
        "url": "http://github.com/tracardi/trello-microservice",
        "email": "office@tracardi.com",
    },
    docs_url=None,
    redoc_url=None,
)

application.mount("/uix",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "uix")),
                  name="uix")

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(service_endpoint.router)
application.include_router(auth_endpoint.router)


@application.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:

        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        return JSONResponse(status_code=500,
                            headers={
                                "access-control-allow-credentials": "true",
                                "access-control-allow-origin": "*"
                            },
                            content={"details": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:application", host="0.0.0.0", port=20000, log_level="info")
