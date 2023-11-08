from pydantic import BaseModel


class Member(BaseModel):
    code: str
    name: str
    area: str
    age: int
    email: str
    role: str
    state: int
    neg_score: int
