from fastapi import FastAPI
from fastapi.openapi.models import HTTPBase
from fastapi.params import Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.routers import user, item, image_interaction, visualglm

app = FastAPI()
security = HTTPBasic()

app.include_router(user.router)
app.include_router(item.app)
app.include_router(image_interaction.app)
app.include_router(visualglm.router)
