from pydantic import BaseModel
from typing import List
from Schedule import Schedule

class PsychologistSchedule(BaseModel):
    member_code: str
    schedule: List[Schedule]