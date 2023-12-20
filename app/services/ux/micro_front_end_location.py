from pydantic import BaseModel, AnyHttpUrl


class MicroFrontEndLocation(BaseModel):
    uix_mf_source: AnyHttpUrl

    @staticmethod
    def create():
        return MicroFrontEndLocation(
            uix_mf_source=AnyHttpUrl("http://localhost:20000")
        )
