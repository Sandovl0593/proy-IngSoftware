from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.psychologist_schedule import routes_psychologist_schedule
from routes.emotion_log import routes_emotion_log
from routes.graphic import routes_graphic
from routes.emotion import routes_emotion
from routes.member import routes_member
from routes.area import routes_area
from routes.configuracion import routes_configuracion
from routes.login import routes_login
from database.db import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_psychologist_schedule, prefix="/psychologist_schedule")
app.include_router(routes_emotion_log, prefix="/emotion_log")
app.include_router(routes_graphic, prefix="/graphic")
app.include_router(routes_emotion, prefix="/emotion")
app.include_router(routes_member, prefix="/member")
app.include_router(routes_area, prefix="/area")
app.include_router(routes_configuracion, prefix="/configuracion")
app.include_router(routes_login, prefix="/user")
#create_tables()