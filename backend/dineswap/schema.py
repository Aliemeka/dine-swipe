from pydantic import BaseModel


class CreateRoomSchema(BaseModel):
    name: str
    note: str | None
    restaurants: list[int]


class JoinRoomSchema(BaseModel):
    shortcode: str
