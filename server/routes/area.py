from server.controllers.area_ctrl import get_areas
from fastapi import APIRouter
from typing import Optional

routes_area = APIRouter()


@routes_area.get('/all')
def get_all() -> Optional[dict]:
    return get_areas()
