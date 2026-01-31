import requests
from twocaptcha import TwoCaptcha
import os
from typing import Tuple

from google.cloud import storage


def solve_captcha(site_key, url):
    solver = TwoCaptcha(os.getenv("RECAPTCHA_API_KEY"))
    result = solver.recaptcha(sitekey=site_key, url=url)
    print(f"Solved reCaptcha, ID: {result['captchaId']}")
    return result["code"]


def get_country_id(country_name: str):
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
    return response.json()[0]["cca3"]


FIREBASE_GCS_HTTPS_PREFIX = "https://storage.googleapis.com/"


def assert_firebase_gcs_https_url(url: str) -> None:
    if not isinstance(url, str) or not url.startswith(FIREBASE_GCS_HTTPS_PREFIX):
        raise ValueError(
            f"Invalid document URL. Expected prefix '{FIREBASE_GCS_HTTPS_PREFIX}', got: {url!r}"
        )


def extract_bucket_and_blob_from_firebase_gcs_url(url: str) -> Tuple[str, str]:
    assert_firebase_gcs_https_url(url)
    remainder = url[len(FIREBASE_GCS_HTTPS_PREFIX):]
    bucket, sep, blob_path = remainder.partition("/")
    if not sep or not bucket or not blob_path:
        raise ValueError(f"Invalid GCS URL shape: {url!r}")
    return bucket, blob_path


def download_bytes_from_firebase_gcs_url(url: str) -> bytes:
    bucket_name, blob_path = extract_bucket_and_blob_from_firebase_gcs_url(url)
    client = storage.Client(project=os.getenv("GCP_PROJECT_ID"))
    blob = client.bucket(bucket_name).blob(blob_path)
    if not blob.exists():
        raise FileNotFoundError(f"File not found in GCS: {url}")
    return blob.download_as_bytes()
