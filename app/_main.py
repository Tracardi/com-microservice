import uvicorn

uvicorn.run("app.server:application", host="0.0.0.0", port=20000, log_level="info")
