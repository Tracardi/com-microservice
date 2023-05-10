from app.repo.services import repo


# @repo.plugin(id="test")
# def xxx(payload):
#     print("insizde")
#     return True

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.server:application", host="0.0.0.0", port=20000, log_level="info")
