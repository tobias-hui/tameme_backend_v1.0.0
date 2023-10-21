import replicate
import os
from app.services.translation import translate_to_english


def icon_generation(text: str):
  # translate toneglish
  en_text = translate_to_english(text)
  # create icon using replicate
  output = replicate.run(
      "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061",
      input={
          "prompt":
          f"masterpiece, best quality, illustration, {en_text}, anime icon, white background，props and items",
          "negative_prompt":
          "lowres, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name",
          "width": 256,
          "height": 256
      })
  return output
