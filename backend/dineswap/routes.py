from typing import Sequence

from fastapi import APIRouter, HTTPException, Request

from .schema import CreateRoomSchema, VoteOnRestaurantSchema
from .models import Room, Restaurant
import dineswap.crud as crud

router = APIRouter()

@router.post("/create-room")
def create_room(payload: CreateRoomSchema) -> Room:
    if len(payload.restaurants) < 2:
        raise HTTPException(
            status_code=400, detail="You must pass at least two restaurants"
        )

    return crud.create_room(payload)


@router.get("/room/{shortcode}")
def join_room(shortcode: str, request: Request) -> Room:
    return crud.join_room(shortcode, request)


@router.get("/room/{room_id}/restaurants")
def get_restaurants(room_id: int) -> Sequence[Restaurant]:
    return crud.get_room_restaurants(room_id)


@router.post("/room/vote")
def vote(payload: VoteOnRestaurantSchema, request: Request):
    return crud.vote_on_restaurant(payload, request)

@router.get("/room/{room_id}/result")
def get_vote_results():
    pass

@router.get("/get-restaurants")
def get_resturants() -> Sequence[Restaurant]:
    return crud.get_resturants()
