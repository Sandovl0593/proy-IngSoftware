from controllers.psychologist_schedule_ctrl import get_psychologist_schedules_details
from fastapi import APIRouter
from typing import Optional

routes_psychologist_schedule = APIRouter()

@routes_psychologist_schedule.get('/all/details')
def get_details() -> Optional[dict]: 
    return get_psychologist_schedules_details()
