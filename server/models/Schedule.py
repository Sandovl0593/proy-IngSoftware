from pydantic import BaseModel
from typing import List

class Schedule(BaseModel):
    day: str
    hours: List[str]