from app.services.translation import translate_to_english
import app.utils.mj as mj
import os

mj_api_key = os.environ['MJ_API_KEY']


def avatar_create(text):
  #translate to english
  text = translate_to_english(text)
  #add text to prompt
  prompt = f'masterpiece, close up, a black cat palying a game console, {text}, anime art, charming illustrations, best quality, Healing --niji 5'
  #make imagine request
  max_retries = 5
  retries = 0
  while retries < max_retries:
    task_id = mj.make_imagine_request(mj_api_key, prompt)
    if task_id is not None:
      break
    else:
      retries += 1
      print(f'Failed to get task id, retrying {retries}/{max_retries}...')
  if retries == max_retries:
    print('Failed to get task id, aborting')
    return None

  #fetch request
  # make sure the imagine process has finished
  while True:
    image_url = mj.fetch_request(mj_api_key, task_id)
    if image_url is not None:
      break
    elif image_url is None:
      print('Imagine process failed, exiting...')
      raise SystemExit('Imagine process failed')
  return task_id


def avatar_upscale(task_id, index):
  task_id = mj.make_upscale_request(mj_api_key, task_id, index)
  # make sure the upscale task sucessfully
  if task_id is not None:
    pass
  elif task_id is None:
    print('Upscale process failed, exiting...')
    raise SystemExit('Upscale process failed')
  # make sure the upscale process has finished
  while True:
    upscale_image_url = mj.fetch_request(mj_api_key, task_id)
    if upscale_image_url is not None:
      break
    elif upscale_image_url is None:
      print('Upscale process failed, exiting...')
      raise SystemExit('Upscale process failed')
  return upscale_image_url


def mj_generation(text):
  #create avatar
  task_id = avatar_create(text)
  print(f'\navatar create successful task_id is {task_id}\n')
  #upscale avatar and remove background
  index = random.randint(1, 4)
  while True:
    print(f'upsclae index is {index} and task_id is {task_id}')
    upscale_image_url = avatar_upscale(task_id, index)
    if upscale_image_url is not None:
      break
    elif upscale_image_url is None:
      print('Upscale process failed, exiting...')
      raise SystemExit('Upscale process failed')
  print(f'upscale_image_url is {upscale_image_url}')
  return upscale_image_url
