import requests
from PIL import Image
from io import BytesIO
import hashlib
import os


def download_image(image_url):
  response = requests.get(image_url)
  response.raise_for_status()  # 检查请求是否成功
  image = Image.open(BytesIO(response.content))
  image_hash = hashlib.sha256(response.content).hexdigest()
  image_path = f'./examples/{image_hash}.png'
  image.save(image_path)
  return os.path.abspath(image_path)
