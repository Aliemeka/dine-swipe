from typing import Sequence

from fastapi import APIRouter, HTTPException, Request

from .schema import CreateRoomSchema, JoinRoomSchema
from .models import Room, Restaurant
import crud

router = APIRouter()

@router.post("/create-room")
def create_room(payload: CreateRoomSchema) -> Room:
    if len(payload.restaurants) < 2:
        raise HTTPException(
            status_code=400, detail="You must pass at least two restaurants"
        )

    return crud.create_room(payload)


@router.post("/join-room")
def join_room(payload: JoinRoomSchema, request: Request) -> Room:
    return crud.join_room(payload, request)


@router.post("room/{room_id}/vote")
def vote(payload):
    pass

@router.get("room/{room_id}/result")
def get_vote_results():
    pass

@router.get("/get-restaurants")
def get_resturants() -> Sequence[Restaurant]:
    return crud.get_resturants()
