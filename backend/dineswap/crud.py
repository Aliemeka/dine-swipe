from typing import Sequence

from fastapi import Request, HTTPException
from sqlmodel import Session, select

from .db import engine, session
from .schema import CreateRoomSchema, VoteOnRestaurantSchema
from .models import Restaurant, Room, RoomRestaurants, AppSession, Vote
from .utils import generate_session_from_ip, validate_restaurant_votes


def create_room(payload: CreateRoomSchema):
    with session() as s:
        room = Room(name=payload.name, note=payload.note)
        s.add(room)
        s.commit()
        room_restuarants = (
            RoomRestaurants(room_id=room.id, restaurant_id=restaurant)
            for restaurant in payload.restaurants
        )
        s.add_all(room_restuarants)
        s.commit()
        s.refresh(room)
        return room


def join_room(shortcode: str, request: Request) -> Room:
    ip = request.client.host if request.client else None
    if ip is None:
        raise HTTPException(status_code=403, detail="client information is not known")
    session_id = generate_session_from_ip(ip)

    with session() as s:
        room = (
            s.execute(select(Room).where(Room.shortcode == shortcode)).scalar()
        )
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")

        app_session = s.execute(
            select(AppSession).where(AppSession.session_id == session_id)
        ).scalar()
        if app_session is None:
            app_session = AppSession(session_id=session_id)
            s.add(app_session)
            s.commit()

        s.refresh(room)
    return room

def vote_on_restaurant(payload: VoteOnRestaurantSchema, request: Request):
    if len(payload.votes) > 3:
        raise HTTPException(status_code=400, detail="you can't vote on more than 3 choices")

    if not validate_restaurant_votes(payload.votes):
        raise HTTPException(status_code=400, detail="validation failed for user vote")

    ip = request.client.host if request.client else None
    if ip is None:
        raise HTTPException(status_code=403, detail="client information is not known")
    session_id = generate_session_from_ip(ip)

    with Session(engine) as session:
        app_session = session.exec(
            select(AppSession).where(AppSession.session_id == session_id)
        ).first()
        if app_session is None:
            raise HTTPException(status_code=400, detail="session not found for this user. did you join the room?")

        room = (
            session.execute(select(Room).where(Room.id == payload.room_id)).scalar()
        )
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")

        if not room.valid_deadline():
            raise HTTPException(status_code=400, detail="Deadline elapsed.")

        user_voted = session.execute(select(Vote).where(Vote.room_id == payload.room_id and Vote.voter_id == app_session.id)).first()
        if user_voted:
            raise HTTPException(status_code=403, detail="Already voted in this room")

        votes = [
            Vote(points=vote.points, room_id=payload.room_id, resturant_id=vote.id, voter_id=app_session.id) for vote in payload.votes
        ]

        session.add_all(votes)
        session.commit()



def get_room_restaurants(room_id: int) -> Sequence[Restaurant]:
    with Session(engine) as session:
        restaurants = session.exec(
            select(Restaurant).join(RoomRestaurants).where(RoomRestaurants.room_id == room_id)
        ).all()
        return restaurants

def get_resturants() -> Sequence[Restaurant]:
    with Session(engine) as session:
        restaurants = session.exec(select(Restaurant)).all()
        return restaurants
