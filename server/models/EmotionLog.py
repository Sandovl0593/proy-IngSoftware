from pydantic import BaseModel


class EmotionLog(BaseModel):
    member_code: str
    timestamp: str
    emotion: str
