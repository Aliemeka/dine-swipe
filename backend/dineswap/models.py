from datetime import datetime, timedelta

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text

from .utils import generate_shortcode


class AppSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
    )

class RoomRestaurants(SQLModel, table=True):
    room_id: int | None = Field(default=None, foreign_key="room.id", primary_key=True)
    restaurant_id: int | None = Field(
        default=None, foreign_key="restaurant.id", primary_key=True
    )


class Restaurant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    image: str
    rating: int = Field(gt=0, lt=6)
    created_at: datetime = Field(
        default_factory=datetime.now,
    )


class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    shortcode: str = Field(default_factory=generate_shortcode, index=True, unique=True)
    note: str | None = Field(sa_column=Column(Text))
    deadline: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(hours=1)
    )
    restaurants: list[Restaurant] = Relationship(link_model=RoomRestaurants)
    created_at: datetime = Field(
        default_factory=datetime.now,
    )


class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    points: int = Field(gt=0, index=True)
    room_id: int = Field(foreign_key="room.id")
    resturant_id: int = Field(foreign_key="restaurant.id")
    voter_id: int = Field(foreign_key="appsession.id")
    created_at: datetime = Field(
        default_factory=datetime.now,
    )
