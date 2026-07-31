import os
import requests

API = "https://graph.facebook.com/v25.0"
PAGE_ID = "1079840611881494"
TARGET = "https://jmswebdesign.com.au/"
TOKEN = os.environ["META_PAGE_TOKEN_1079840611881494"]


def page():
    response = requests.get(
        f"{API}/{PAGE_ID}",
        params={"fields": "name,website", "access_token": TOKEN},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

before = page()
if before.get("website") != TARGET:
    response = requests.post(
        f"{API}/{PAGE_ID}",
        data={"website": TARGET, "access_token": TOKEN},
        timeout=30,
    )
    response.raise_for_status()

after = page()
if after.get("website") != TARGET:
    raise RuntimeError("Facebook Page website field did not retain canonical HTTPS URL")
print({"before": before.get("website"), "after": after.get("website")})
