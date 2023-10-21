import replicate
import os
from app.services.translation import translate_to_chinese


def analyze_process(url):
  print(f'\nanalyzing image: {url}')
  eng_output = replicate.run(
      "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
      input={
          "image": url,
          "caption": True,
          "temperature": 0.5
      })
  output = translate_to_chinese(eng_output)
  print(f'analyzed caption: {output}\n')
  return output
