import os
import json
from transformers import AutoTokenizer, AutoModel
from fastapi.routing import APIRouter
import datetime
import torch
from services import download_image
from models import visualglm

tokenizer = AutoTokenizer.from_pretrained("THUDM/visualglm-6b",
                                          trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/visualglm-6b",
                                  trust_remote_code=True).half().cuda()

router = APIRouter(tags=["image interaction"])


@router.post('/visualglm/')
async def visual_glm(data: visualglm):
  query = data.text
  image_url = data.image_url
  history = data.history

  # download image form url
  image_path = download_image(image_url)  # 下载图像

  with torch.no_grad():
    result = model.stream_chat(tokenizer, image_path, query, history=history)

  last_result = None
  for value in result:
    last_result = value
  answer = last_result[0]

  if os.path.isfile(image_path):  # 检查临时图像文件是否存在，如果存在则删除
    os.remove(image_path)

  now = datetime.datetime.now()
  time = now.strftime("%Y-%m-%d %H:%M:%S")
  response = {
      "result": answer,
      "history": history,
      "status": 200,
      "time": time
  }
  return response
