from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    original_url: HttpUrl
    short_code: str

    model_config = {
        "from_attributes": True
    }