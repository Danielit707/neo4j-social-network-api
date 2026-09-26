from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.graph_model import create_post, comment_on_post
from app.routes.auth import get_current_user

router = APIRouter()

class PostIn(BaseModel):
    content: str
    media_url: str = None

@router.post("/")
def post_create(data: PostIn, me=Depends(get_current_user)):
    p = create_post(me["email"], data.content, data.media_url)
    return {"status":"ok", "post": dict(p["p"]) if p else None}

class CommentIn(BaseModel):
    post_id: str
    content: str

@router.post("/comment")
def comment(data: CommentIn, me=Depends(get_current_user)):
    c = comment_on_post(me["email"], data.post_id, data.content)
    return {"status":"ok", "comment": dict(c["c"]) if c else None}
