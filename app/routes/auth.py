from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.models.graph_model import create_user_node, get_user_by_email_record, get_user_node_props_by_email
from app.utils.auth_utils import hash_password, verify_password, create_access_token, decode_token

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if get_user_by_email_record(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    create_user_node(user.username, user.email, hashed)
    return {"username": user.username, "email": user.email}

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(data: LoginIn):
    rec = get_user_by_email_record(data.email)
    if not rec:
        raise HTTPException(status_code=404, detail="User not found")
    node = rec['u']
    if not verify_password(data.password, node['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": node['email']})
    return {"access_token": token, "token_type": "bearer"}

# Simple dependency to get current user from Authorization: Bearer <token>
from fastapi import Header

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    user = get_user_node_props_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
