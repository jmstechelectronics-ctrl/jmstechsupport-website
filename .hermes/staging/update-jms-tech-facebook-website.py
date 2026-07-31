import os
import requests

API = "https://graph.facebook.com/v25.0"
PAGE_ID = "838133966059924"
TOKEN = os.environ.get("JMS_META_API_TECH_ACCESS_TOKEN") or os.environ["META_PAGE_TOKEN_838133966059924"]
TARGET = "https://jmstechsupport.com.au/"

before = requests.get(
    f"{API}/{PAGE_ID}",
    params={"fields": "name,website,link", "access_token": TOKEN},
    timeout=45,
)
before.raise_for_status()
update = requests.post(
    f"{API}/{PAGE_ID}",
    data={"website": TARGET, "access_token": TOKEN},
    timeout=45,
)
after = requests.get(
    f"{API}/{PAGE_ID}",
    params={"fields": "name,website,link", "access_token": TOKEN},
    timeout=45,
)
print({
    "before_website": before.json().get("website"),
    "update_http_status": update.status_code,
    "update_success": bool(update.json().get("success")),
    "update_error": update.json().get("error", {}).get("message"),
    "after_website": after.json().get("website"),
    "page_link": after.json().get("link"),
})
