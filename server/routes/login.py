from controllers.login_ctrl import login as login_ctrl
from fastapi import APIRouter
from typing import Optional

routes_login = APIRouter()

@routes_login.get("/{id}/{password}")
def login(id: str, password: str) -> Optional[dict]:
    return login_ctrl(id, password)