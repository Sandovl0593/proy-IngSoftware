from controllers.recommendation_ctrl import get_recommedation
from fastapi import APIRouter
from typing import Optional

routes_recommendation = APIRouter()

@routes_recommendation.get('/all')
def get_all() -> Optional[dict]:
    return get_recommedation()
