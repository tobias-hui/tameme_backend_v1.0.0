from fastapi import FastAPI, HTTPException, status, Path
from fastapi.routing import APIRouter
from app.services.image_analyze import analyze_process
from app.services.mj_generation import mj_generation
from app.services.icon_generation import icon_generation
from app.models.txt_request import TxtRequest

app = APIRouter(tags=["image interaction"])


@app.post("/image/analyze/")
async def analyze_api(request: TxtRequest):
  try:
    output = analyze_process(request.input)
    return {"output": output}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


@app.post("/image/mj/")
async def mj(request: TxtRequest):
  try:
    image_url = mj_generation(request.input)
    return {"image_url": image_url}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


@app.post("/image/icon/")
async def icon(request: TxtRequest):
  try:
    output = icon_generation(request.input)
    return {"output": output}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
