from pydantic import BaseModel

class Emotion(BaseModel):
    name: str
    score: int
