from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import textwrap

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1350
BG = "#071722"
PANEL = "#0E2635"
BLUE = "#0B75B8"
PALE_BLUE = "#B8E2FA"
WHITE = "#F7FAFC"
MUTED = "#9EB6C5"
GOLD = "#F6C453"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REVIEWS = [
    {
        "key": "38",
        "filename": "review-tom-m.jpg",
        "name": "Tom M.",
        "service": "Security cameras",
        "excerpt": "I fully recommend him and his product.",
        "source_text": "I met Josh as a result of his letter drop in my area. He was and is just brilliant. He installed my cameras at my home, assisted with the set-up and has on numerous occasions provided great after care. The camera's are just what we needed. I fully recommend him and his product. All the best Josh.",
        "published_relative_date": "3 months ago",
    },
    {
        "key": "39",
        "filename": "review-mekala-h.jpg",
        "name": "Mekala H.",
        "service": "Slow internet and Wi-Fi",
        "excerpt": "By the time he left, my internet was so much faster. The difference was massive.",
        "source_text": "Josh came over to fix my internet because it was honestly driving me insane with how slow it was. He didn’t just have a quick look and leave, he actually took the time to figure out what was going on and explain it to me in a way I could understand. By the time he left, my internet was so much faster. The difference was massive. What I really appreciated was that he gave me proper advice, not just a quick fix. You can tell he knows what he’s doing and actually cares about getting it right. Highly recommend.",
        "published_relative_date": "3 months ago",
    },
    {
        "key": "40",
        "filename": "review-wendi-m.jpg",
        "name": "Wendi M.",
        "service": "Reliable house calls",
        "excerpt": "Josh was very professional, he knew what he was talking about. Each time he turned up when he said he would.",
        "source_text": "Josh was very professional, he knew what he was talking about. Each time he turned up when he said he would.",
        "published_relative_date": "a month ago",
    },
    {
        "key": "41",
        "filename": "review-wendy-d.jpg",
        "name": "Wendy D.",
        "service": "Security cameras",
        "excerpt": "Great service great products and great after service",
        "source_text": "I recently had security cameras installed and cannot recommend highly enough. Great service great products and great after service",
        "published_relative_date": "2 months ago",
    },
    {
        "key": "42",
        "filename": "review-helen-b.jpg",
        "name": "Helen B.",
        "service": "External security camera",
        "excerpt": "Very happy with my external camera, great peace of mind",
        "source_text": "Very happy with my external camera, great peace of mind.....thanks Josh 😊",
        "published_relative_date": "5 months ago",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, outer, inner):
    import math
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = outer if i % 2 == 0 else inner
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def wrapped_lines(draw, text, typeface, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=typeface)[2] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def make_card(review):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((55, 55, W - 55, H - 55), radius=44, fill=PANEL, outline="#1D4054", width=3)
    draw.rounded_rectangle((84, 96, 342, 160), radius=28, fill="#133C53")
    draw.text((111, 111), "GOOGLE REVIEW", font=font(FONT_BOLD, 27), fill=PALE_BLUE)
    for index in range(5):
        cx = 109 + index * 55
        draw.polygon(star_points(cx, 228, 19, 8), fill=GOLD)
    draw.text((84, 298), review["service"].upper(), font=font(FONT_BOLD, 25), fill="#63B9E8")
    quote_font = font(FONT_BOLD, 65)
    lines = wrapped_lines(draw, f'“{review["excerpt"]}”', quote_font, W - 168)
    line_height = 86
    total_height = len(lines) * line_height
    y = 570 - total_height // 2
    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=quote_font)[2]
        draw.text(((W - line_width) / 2, y), line, font=quote_font, fill=WHITE)
        y += line_height
    draw.line((84, 988, W - 84, 988), fill="#1E4A61", width=2)
    draw.text((84, 1026), "5-star Google review", font=font(FONT_REGULAR, 31), fill=MUTED)
    draw.text((84, 1082), review["name"], font=font(FONT_BOLD, 36), fill=WHITE)
    draw.text((84, 1196), "JMS TECH SUPPORT", font=font(FONT_BOLD, 33), fill=WHITE)
    draw.text((84, 1242), "Yamba  •  Maclean  •  Clarence Valley", font=font(FONT_REGULAR, 25), fill=PALE_BLUE)
    image.save(OUT / review["filename"], "JPEG", quality=90, optimize=True)


for review in REVIEWS:
    make_card(review)

provenance = {
    "source": "Google Maps public reviews for JMS Tech Support",
    "source_url": "https://www.google.com/maps?cid=12452262121885535819&hl=en-AU",
    "usage_rules": [
        "The visible excerpt is an exact contiguous excerpt of the source review.",
        "Reviewer names are reduced to first name and surname initial.",
        "Every featured review is five stars.",
        "Do not pair a review with an unrelated job image as though it documents that job.",
    ],
    "reviews": REVIEWS,
}
(OUT / "review-provenance.json").write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n")
