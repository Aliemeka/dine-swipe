from typing import Sequence

from fastapi import Request, HTTPException
from sqlmodel import Session, select

from .db import engine, session
from .schema import CreateRoomSchema, JoinRoomSchema
from .models import Restaurant, Room, RoomRestaurants, AppSession
from .utils import generate_session_from_ip


def create_room(payload: CreateRoomSchema):
    with session() as s:
        room = Room(name=payload.name, note=payload.note)
        s.add(room)
        s.commit()
        s.refresh(room)
        room_restuarants = (
            RoomRestaurants(room_id=room.id, restaurant_id=restaurant)
            for restaurant in payload.restaurants
        )
        s.add_all(room_restuarants)
        s.commit()

    return room


def join_room(payload: JoinRoomSchema, request: Request) -> Room:
    ip = request.client.host if request.client else None
    if ip is None:
        raise HTTPException(status_code=403, detail="client information is not known")
    session_id = generate_session_from_ip(ip)

    with session() as s:
        room = (
            s.execute(select(Room).where(Room.shortcode == payload.shortcode)).scalar()
        )
        if room is None:
            raise HTTPException(status_code=404, detail="Not found")

        app_session = s.execute(
            select(AppSession).where(AppSession.session_id == session_id)
        ).scalar()
        if session is None:
            app_session = AppSession(session_id=session_id)
            s.add(app_session)

        s.commit()

    return room


def get_resturants() -> Sequence[Restaurant]:
    with Session(engine) as session:
        restaurants = session.exec(select(Restaurant)).all()
        return restaurants
