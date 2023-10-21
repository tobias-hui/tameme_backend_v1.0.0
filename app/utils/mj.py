import requests
import time


def make_imagine_request(api_key, prompt):
  endpoint = "https://api.midjourneyapi.xyz/mj/v2/imagine"
  headers = {
      'X-API-KEY': api_key,
      'Content-Type': 'application/json',
  }
  payload = {"prompt": prompt.strip(), "process_mode": "fast"}
  response = requests.post(endpoint, headers=headers, json=payload).json()
  # check if api key is valid
  if "message" in response and response["message"] == "Invalid API key":
    print('Invalid API key')
    return None
  # check if api key has enough credits
  if "message" in response and response["message"] == "Insufficient token":
    print('Insufficient token')
    return None

  task_id = response.get("task_id", None)
  if task_id is not None:
    print(f'Task id for prompt \'{prompt}\': {task_id}')
  else:
    print('Failed to get task id')

  return task_id


def make_upscale_request(api_key, original_task_id, index):
  endpoint = "https://api.midjourneyapi.xyz/mj/v2/upscale"
  headers = {
      'X-API-KEY': api_key,
      'Content-Type': 'application/json',
  }
  payload = {"origin_task_id": original_task_id, "index": str(index)}
  response = requests.post(endpoint, headers=headers, json=payload).json()
  task_id = response.get("task_id", None)
  if task_id is not None:
    print(f'Upscale Task id for prompt: {task_id}')
  else:
    print('Failed to get task id')

  return task_id


def make_outpaint_request(api_key, prompt, original_task_id):
  endpoint = "https://api.midjourneyapi.xyz/mj/v2/outpaint"
  headers = {
      'X-API-KEY': api_key,
      'Content-Type': 'application/json',
  }
  payload = {
      "origin_task_id": original_task_id,
      "zoom_ratio": "2",
      "prompt": prompt.strip(),
  }
  response = requests.post(endpoint, headers=headers, json=payload).json()
  task_id = response.get("task_id", None)
  if task_id is not None:
    print(f'Task id for prompt \'{prompt}\': {task_id}')
  else:
    print('Failed to get task id')

  return task_id


def make_vary_request(api_key, prompt, original_task_id):
  endpoint = "https://api.midjourneyapi.xyz/mj/v2/variation"
  headers = {
      'X-API-KEY': api_key,
      'Content-Type': 'application/json',
  }
  payload = {
      "origin_task_id": original_task_id,
      'index': 'high_variation',
      'prompt': prompt,
      'aspect_ratio': '1:1'
  }
  response = requests.post(endpoint, headers=headers, json=payload).json()
  task_id = response.get("task_id", None)
  if task_id is not None:
    print(f'Task id for prompt \'{prompt}\': {task_id}')
  else:
    print('Failed to get task id')

  return task_id


def fetch_request(api_key, task_id, max_retries=35):
  endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"
  headers = {'X-API-KEY': api_key}
  payload = {"task_id": task_id}

  retries = 0
  while True:
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
      response_json = response.json()
      status = response_json.get('status', '')
      if status == 'finished':
        discord_url = response_json['task_result'].get('discord_image_url', '')
        return discord_url
      elif status == 'failed':
        print('Task failed. Stopping retrieval attempts.')
        return None
      else:
        print('Result not ready yet, retrying in 10 seconds...')
    else:
      print('Failed to fetch result, retrying in 10 seconds...')
      retries += 1
      if retries > max_retries:
        raise Exception('Failed to fetch result after maximum retries.')
    time.sleep(10)
