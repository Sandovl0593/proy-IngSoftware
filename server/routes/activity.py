from controllers.activity_ctrl import get_activities, get_activity
from fastapi import APIRouter
from typing import Optional

routes_activity = APIRouter()

@routes_activity.get('/all')
def get_all() -> Optional[dict]:
    return get_activities()

@routes_activity.get('/{activity_id}')
def get(activity_id: str) -> Optional[dict]:
    return get_activity(activity_id)