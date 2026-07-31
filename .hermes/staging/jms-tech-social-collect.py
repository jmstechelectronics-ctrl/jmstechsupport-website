import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

API = "https://graph.facebook.com/v25.0"
PAGE_ID = "838133966059924"
IG_ID = "17841478672968832"
REPORTS = Path("/home/josh/kramer-data/reports")
REPORTS.mkdir(parents=True, exist_ok=True)
TOKEN = os.environ.get("JMS_META_API_TECH_ACCESS_TOKEN") or os.environ["META_PAGE_TOKEN_838133966059924"]


def graph(path, params=None):
    response = requests.get(
        f"{API}/{path.lstrip('/')}",
        params={**(params or {}), "access_token": TOKEN},
        timeout=45,
    )
    if not response.ok:
        detail = response.json().get("error", {}).get("message", "unknown Graph API error")
        raise RuntimeError(f"Graph API request failed for {path}: {detail}")
    return response.json()


def all_pages(path, params):
    result = []
    payload = graph(path, params)
    while True:
        result.extend(payload.get("data", []))
        next_url = payload.get("paging", {}).get("next")
        if not next_url:
            return result
        response = requests.get(next_url, timeout=45)
        if not response.ok:
            detail = response.json().get("error", {}).get("message", "unknown Graph API error")
            raise RuntimeError(f"Graph API pagination failed for {path}: {detail}")
        payload = response.json()


def count_summary(item, name):
    return int(item.get(name, {}).get("summary", {}).get("total_count", 0))


def safe_excerpt(value, limit=220):
    return " ".join((value or "").split())[:limit]


captured_at = datetime.now(timezone.utc).isoformat()
page = graph(PAGE_ID, {"fields": "id,name,link,website,fan_count,followers_count"})
instagram = graph(IG_ID, {"fields": "id,username,followers_count,media_count"})
fb_collection_error = None
try:
    fb_posts = all_pages(
        f"{PAGE_ID}/feed",
        {
            "limit": 100,
            "fields": "id,created_time,message,permalink_url,reactions.limit(0).summary(true),comments.limit(0).summary(true)",
        },
    )
except RuntimeError as exc:
    fb_posts = []
    fb_collection_error = str(exc)
ig_media = all_pages(
    f"{IG_ID}/media",
    {
        "limit": 100,
        "fields": "id,timestamp,caption,permalink,like_count,comments_count,media_type",
    },
)

baseline = {
    "captured_at_utc": captured_at,
    "source": "Meta Graph API read-only collection",
    "facebook": {
        "page": {key: page.get(key) for key in ("id", "name", "link", "website", "fan_count", "followers_count")},
        "collection_error": fb_collection_error,
        "post_count_collected": len(fb_posts),
        "posts": [
            {
                "id": post["id"],
                "created_time": post.get("created_time"),
                "permalink_url": post.get("permalink_url"),
                "excerpt": safe_excerpt(post.get("message")),
                "reactions": count_summary(post, "reactions"),
                "comments": count_summary(post, "comments"),
                "shares": 0,
            }
            for post in fb_posts
        ],
    },
    "instagram": {
        "account": {key: instagram.get(key) for key in ("id", "username", "followers_count", "media_count")},
        "media_count_collected": len(ig_media),
        "media": [
            {
                "id": media["id"],
                "timestamp": media.get("timestamp"),
                "permalink": media.get("permalink"),
                "excerpt": safe_excerpt(media.get("caption")),
                "likes": int(media.get("like_count", 0)),
                "comments": int(media.get("comments_count", 0)),
                "media_type": media.get("media_type"),
            }
            for media in ig_media
        ],
    },
}

instagram_likes = [entry["likes"] for entry in baseline["instagram"]["media"]]
baseline["instagram"]["summary"] = {
    "average_likes": round(sum(instagram_likes) / len(instagram_likes), 2) if instagram_likes else 0,
    "posts_with_comments": sum(1 for entry in baseline["instagram"]["media"] if entry["comments"]),
}

keywords = ("wi-fi", "wifi", "backup", "password", "chromecast", "camera", "printer", "scam", "facebook")
audit_rows = []
for platform, entries in (("facebook", baseline["facebook"]["posts"]), ("instagram", baseline["instagram"]["media"])):
    for entry in entries:
        text = entry.get("excerpt", "")
        flags = [word for word in keywords if word in text.lower()]
        audit_rows.append(
            {
                "platform": platform,
                "url": entry.get("permalink_url") or entry.get("permalink"),
                "published_at": entry.get("created_time") or entry.get("timestamp"),
                "excerpt": text,
                "topic_flags": flags,
                "engagement": {key: entry[key] for key in ("reactions", "comments", "shares", "likes") if key in entry},
                "recommendation": "retain_pending_human_review",
                "reason": "No deletion decision is made automatically. Low engagement alone is insufficient evidence for removal.",
            }
        )

audit = {
    "captured_at_utc": captured_at,
    "scope": "All retrievable Facebook Page posts and Instagram Business media from the authorised Meta account.",
    "deletion_policy": "No automated archive, hide, edit, or delete action was taken.",
    "records": audit_rows,
}

baseline_path = REPORTS / "jms-tech-social-baseline-2026-07-31.json"
audit_path = REPORTS / "jms-tech-social-post-audit-2026-07-31.json"
baseline_path.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n")
audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "baseline": str(baseline_path),
    "audit": str(audit_path),
    "facebook_posts": len(fb_posts),
    "instagram_media": len(ig_media),
    "facebook_followers": page.get("followers_count"),
    "instagram_followers": instagram.get("followers_count"),
}, indent=2))
