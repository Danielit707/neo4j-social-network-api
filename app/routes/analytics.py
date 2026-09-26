from fastapi import APIRouter, Depends

from app.models.graph_model import get_network_stats, get_user_stats
from app.routes.auth import get_current_user

router = APIRouter()


@router.get("/summary")
def summary():
    """Return aggregate counts for the graph."""
    return get_network_stats()


@router.get("/me")
def my_stats(me=Depends(get_current_user)):
    """Return activity counts for the authenticated user."""
    return get_user_stats(me["email"])
