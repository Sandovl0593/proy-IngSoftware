from controllers.configuracion_ctrl import get_configuracion, update_configuracion
from fastapi import APIRouter
from typing import Optional

routes_configuracion = APIRouter()

@routes_configuracion.get('/all')
def get_all() -> Optional[dict]:
    return get_configuracion()


@routes_configuracion.put("/{tipo}/{value}")
def update_tipo_configuracion(tipo: str, new_value: int, tenant_id = 'UTEC') -> Optional[dict]:
    return update_configuracion(tipo, new_value, tenant_id)
