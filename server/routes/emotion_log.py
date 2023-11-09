from controllers.emotion_log_ctrl import get_emotion_logs, get_emotion_logs_member 
from fastapi import APIRouter
from typing import Optional, List

routes_emotion_log = APIRouter()

@routes_emotion_log.get('/member_code/{member_code}/{from_date}')
def get_by_code(member_code: str, from_date) -> Optional[List[dict]]:
    return get_emotion_logs_member(member_code, from_date)

@routes_emotion_log.get('/all/{from_date}')
def get_all(from_date: str) -> Optional[List[dict]]:
    return get_emotion_logs(from_date)