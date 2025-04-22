from pydantic import BaseModel, Field


class CreateRoomSchema(BaseModel):
    name: str
    note: str | None
    restaurants: list[int]


class JoinRoomSchema(BaseModel):
    shortcode: str


class RestaurantVote(BaseModel):
    points: int = Field(gt=0, lt=4)
    id: int

class VoteOnRestaurantSchema(BaseModel):
    votes: list[RestaurantVote]
    room_id: int
