from controllers.configuracion_ctrl import get_configuracion
from fastapi import APIRouter
from typing import Optional

routes_configuracion = APIRouter()

@routes_configuracion.get('/all')
def get_all() -> Optional[dict]:
    return get_configuracion()