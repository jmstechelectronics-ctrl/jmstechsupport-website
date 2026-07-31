import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

API = "https://graph.facebook.com/v25.0"
PAGE_ID = "1079840611881494"
IG_ID = "17841425255631522"
TOKEN = os.environ["META_PAGE_TOKEN_1079840611881494"]
REPORT_DIR = Path("/home/josh/kramer-data/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def graph(path, params=None):
    payload = dict(params or {})
    payload["access_token"] = TOKEN
    response = requests.get(f"{API}/{path.lstrip('/')}", params=payload, timeout=45)
    if not response.ok:
        body = response.json().get("error", {})
        raise RuntimeError(f"Graph GET {path} failed: {body.get('code')} {body.get('message')}")
    return response.json()


def collect(path, fields):
    items = []
    url = f"{API}/{path.lstrip('/')}"
    params = {"access_token": TOKEN, "limit": 100, "fields": fields}
    while url:
        response = requests.get(url, params=params, timeout=45)
        if not response.ok:
            body = response.json().get("error", {})
            raise RuntimeError(f"Graph GET {path} failed: {body.get('code')} {body.get('message')}")
        data = response.json()
        items.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
        params = None
    return items


def safe(call):
    try:
        return {"data": call(), "error": None}
    except RuntimeError as exc:
        return {"data": None, "error": str(exc)}

page = safe(lambda: graph(PAGE_ID, {"fields": "id,name,link,website,fan_count,followers_count,instagram_business_account{id,username}"}))
instagram = safe(lambda: graph(IG_ID, {"fields": "id,username,name,followers_count,follows_count,media_count,website,biography"}))
ig_media = safe(lambda: collect(f"{IG_ID}/media", "id,caption,comments_count,like_count,media_type,media_product_type,permalink,timestamp"))
fb_posts = safe(lambda: collect(f"{PAGE_ID}/feed", "id,message,created_time,permalink_url,reactions.limit(0).summary(true),comments.limit(0).summary(true)"))

if ig_media["data"] is not None:
    media = ig_media["data"]
    ig_media["summary"] = {
        "count": len(media),
        "average_likes": round(sum(item.get("like_count", 0) for item in media) / len(media), 2) if media else 0,
        "average_comments": round(sum(item.get("comments_count", 0) for item in media) / len(media), 2) if media else 0,
        "media_types": {kind: sum(1 for item in media if item.get("media_type") == kind) for kind in sorted({item.get("media_type") for item in media})},
    }

report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "scope": "JMS Web Design social baseline and content sample; read-only assessment",
    "facebook": page,
    "instagram": instagram,
    "instagram_media": ig_media,
    "facebook_posts": fb_posts,
}
path = REPORT_DIR / "jms-web-social-baseline-2026-07-31.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({
    "report": str(path),
    "facebook_page_read": page["error"] is None,
    "instagram_profile_read": instagram["error"] is None,
    "instagram_media": len(ig_media["data"] or []),
    "facebook_posts": len(fb_posts["data"] or []),
}, indent=2))
