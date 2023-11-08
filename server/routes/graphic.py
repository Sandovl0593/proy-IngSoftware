from server.controllers.graphic_ctrl import get_values_main_graphic, get_emotion_area_members_graphic
from fastapi import APIRouter
from typing import Optional

routes_graphic = APIRouter()


@routes_graphic.get('/main/values')
def get_main_graphic() -> Optional[dict]:
    return get_values_main_graphic()


@routes_graphic.get('/main/member_codes/{from_date}/{emotion}/{area}')
def get_member_codes_graphic(from_date: str, emotion: str, area: str) -> Optional[dict]:
    return get_emotion_area_members_graphic(from_date, emotion, area)
