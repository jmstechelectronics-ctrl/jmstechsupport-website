from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path('/home/josh/documents/Business/jmswebdesign.com.au')
OUTPUT = ROOT / '.hermes' / 'staging' / 'jms-web-portfolio-ads'
OUTPUT.mkdir(parents=True, exist_ok=True)

NAVY = '#092b4a'
BLUE = '#1b89da'
INK = '#102033'
PALE = '#eef7ff'
WHITE = '#ffffff'
SIZE = 1254

ITEMS = [
    ('portfolio-a360.png', 'portfolio-a360ds.webp', 'A360 Disability Solutions', 'A clear, accessible website for a disability support business.', 'See what your business could look like.'),
    ('portfolio-jmstech.png', 'portfolio-jmstech.webp', 'JMS Tech Support', 'A local service website built to make booking help straightforward.', 'Clear services. A direct next step.'),
    ('portfolio-leaddrop.png', 'portfolio-leaddrop.webp', 'LeadDrop', 'A purpose-built platform for connecting tradies with real local leads.', 'A technical build, designed around a real workflow.'),
    ('portfolio-clawgauge.png', 'portfolio-clawgauge.webp', 'ClawGauge', 'A live market-monitoring dashboard built for fast, useful decisions.', 'A technical build with the information that matters visible first.'),
]


def font(size, bold=False):
    name = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(name, size)


def wrapped(draw, text, x, y, width, active_font, fill, line_gap=8):
    words = text.split()
    lines, line = [], ''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if draw.textbbox((0, 0), candidate, font=active_font)[2] <= width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for line in lines:
        draw.text((x, y), line, font=active_font, fill=fill)
        y += active_font.size + line_gap
    return y


for filename, source_name, title, description, result_line in ITEMS:
    source = Image.open(ROOT / 'assets' / source_name).convert('RGB')
    canvas = Image.new('RGB', (SIZE, SIZE), PALE)
    draw = ImageDraw.Draw(canvas)

    # Branded header
    draw.rectangle((0, 0, SIZE, 138), fill=WHITE)
    for dx, dy, colour in ((0, 0, NAVY), (45, 0, BLUE), (0, 45, NAVY), (45, 45, BLUE)):
        draw.rounded_rectangle((50 + dx, 30 + dy, 84 + dx, 64 + dy), radius=5, fill=colour)
    draw.text((150, 34), 'JMS', font=font(48, True), fill=NAVY)
    draw.text((150, 84), 'Web Design', font=font(23), fill=INK)
    draw.text((SIZE - 465, 57), 'REAL WEBSITE PREVIEW', font=font(22, True), fill=BLUE)

    # Source preview in a framed browser-like card.
    preview = ImageOps.contain(source, (1120, 550), Image.Resampling.LANCZOS)
    card_x = (SIZE - preview.width) // 2
    card_y = 175
    shadow = 12
    draw.rounded_rectangle((card_x - shadow, card_y - shadow, card_x + preview.width + shadow, card_y + preview.height + shadow), radius=20, fill='#b7d4e9')
    draw.rounded_rectangle((card_x - 5, card_y - 5, card_x + preview.width + 5, card_y + preview.height + 5), radius=14, fill=WHITE)
    canvas.paste(preview, (card_x, card_y))

    y = 770
    draw.text((67, y), title, font=font(42, True), fill=NAVY)
    y += 62
    y = wrapped(draw, description, 67, y, 1115, font(27), INK, 7)
    y += 12
    y = wrapped(draw, result_line, 67, y, 1115, font(25, True), BLUE, 7)

    draw.rounded_rectangle((55, 1080, 1199, 1197), radius=20, fill=NAVY)
    draw.text((90, 1103), 'Starter websites: $349 once + $29/month', font=font(30, True), fill=WHITE)
    draw.text((90, 1145), 'Domain, hosting, email and ongoing support included.', font=font(21), fill='#d9ecfb')
    draw.rounded_rectangle((909, 1100, 1165, 1178), radius=20, fill=BLUE)
    draw.text((946, 1120), 'GET STARTED', font=font(20, True), fill=WHITE)

    output = OUTPUT / filename
    canvas.save(output, optimize=True)
    print(output)
