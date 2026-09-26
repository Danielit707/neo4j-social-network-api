from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.graph_model import create_friendship, add_interest_to_user, get_user_by_email_record
from app.routes.auth import get_current_user

router = APIRouter()

class FriendAction(BaseModel):
    friend_email: str
    bidir: bool = True

@router.post("/friend")
def befriend(action: FriendAction, me=Depends(get_current_user)):
    if not get_user_by_email_record(action.friend_email):
        raise HTTPException(404, "Friend user not found")
    create_friendship(me["email"], action.friend_email, action.bidir)
    return {"status": "ok", "friend_with": action.friend_email}

class InterestIn(BaseModel):
    interest: str

@router.post("/interest")
def add_interest(data: InterestIn, me=Depends(get_current_user)):
    add_interest_to_user(me["email"], data.interest)
    return {"status":"ok", "interest": data.interest}
