import requests
from twocaptcha import TwoCaptcha
import os


def solve_captcha(site_key, url):
    solver = TwoCaptcha(os.getenv("RECAPTCHA_API_KEY"))
    result = solver.recaptcha(sitekey=site_key, url=url)
    print(f"Solved reCaptcha, ID: {result["captchaId"]}")
    return result["code"]


def get_country_id(country_name: str):
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
    return response.json()[0]["cca3"]
