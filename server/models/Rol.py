from pydantic import BaseModel


class Rol(BaseModel):
    name: str
    description: str
