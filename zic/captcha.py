import re

from requests import Session
from google.cloud import vision
from zic.util_types import ZICInsuranceStages


def _normalize_captcha_text(text: str) -> str:
    return re.sub(r"[^A-Za-z]", "", text).upper()


def _ocr_image_bytes(image_bytes: bytes) -> str:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(f"Vision API error: {response.error.message}")
    if not response.text_annotations:
        raise ValueError("No text detected in captcha image")
    return response.text_annotations[0].description.strip()


def crack_captcha(session: Session) -> str:
    response = session.get(ZICInsuranceStages.GetCaptcha.value)
    response.raise_for_status()
    return _normalize_captcha_text(_ocr_image_bytes(response.content))
