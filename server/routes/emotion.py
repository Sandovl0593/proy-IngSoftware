from fastapi import APIRouter
from typing import Optional
from server.controllers.emotion_ctrl import (
    get_emotion_scores, 
    get_emotion_predominant, 
    get_emotion_names
)

routes_emotion = APIRouter()


@routes_emotion.get('/all/scores')
def get_names() -> Optional[dict]:  
    return get_emotion_scores()


@routes_emotion.get('/all/names')
def get_scores() -> Optional[dict]:  
    return get_emotion_names()


@routes_emotion.get('/predominant')
def get_predominant() -> Optional[dict]:  
    return get_emotion_predominant()
