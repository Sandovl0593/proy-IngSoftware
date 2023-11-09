from controllers.member_ctrl import get_member, update_member_state_score, get_members_top_negative, \
    obtener_miembros_no_atendidos, modificar_estado
from fastapi import APIRouter
from typing import Optional

routes_member = APIRouter()

@routes_member.get("/{code}")
def get_by_code(code: str) -> Optional[dict]:
    return get_member(code)

@routes_member.get("/all/top_negative/{limit}")
def get_top_negative(limit: str) -> Optional[dict]:
    return get_members_top_negative(int(limit))

@routes_member.put("/{code}/state/{state}/score")
def update_state_score(code: str, state: str) -> Optional[dict]:
    return update_member_state_score(code, int(state))

@routes_member.get("/all/kmiembros")
def get_kmiembros():
    return obtener_miembros_no_atendidos()

@routes_member.put("/{code}/state/cambiar/{check}")
def update_state(check: bool, code: str) -> Optional[dict]:
    return modificar_estado(check, code)
