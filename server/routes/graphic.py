from controllers.graphic_ctrl import get_data_main_graphic, get_data_face_graphic
from fastapi import APIRouter
from typing import Optional

routes_graphic = APIRouter()


@routes_graphic.get('/{emocion}/{area}/{dias}')
def get_data_graphic(emocion: str, area: str, dias: int, tenant_id = 'UTEC') -> Optional[dict]:
    return get_data_main_graphic(dias, emocion, area, tenant_id)


@routes_graphic.get('/face-graphic')
def get_data_graphic(tenant_id = 'UTEC') -> Optional[dict]:
    return get_data_face_graphic(tenant_id)   
