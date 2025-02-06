import typing

from pydantic import BaseModel

class ImageRequest(BaseModel):
    base64_image: str
    key: str

class ImageResponse(BaseModel):
    solution: str | typing.Any
