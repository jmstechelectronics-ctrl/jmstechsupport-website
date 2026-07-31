from pathlib import Path
import json
import shutil

state_root = Path('/home/josh/kramer/state/jms-tech-autoposter')
plan_path = state_root / 'rotation-plan.json'
brand_state_path = Path('/home/josh/kramer/state/jms-autoposter-v2/brands/tech.json')
assets = state_root / 'images/rotate_images'
source = Path('/home/josh/kramer/state/jms-tech-autoposter/review-provenance.json')

reviews = [
    {
        'rotation_index': '38', 'publish_order': 17.5,
        'title': 'Five-star review: security cameras that fit the job',
        'caption': 'A recent five-star Google review after a security camera installation.\n\n"I fully recommend him and his product."\n\nNeed practical security cameras and proper after-care? JMS Tech Support comes to you across Yamba, Maclean and the Clarence Valley.',
        'image_path': str(assets / 'review-tom-m.jpg'), 'image_filename': 'review-tom-m.jpg',
        'image_url': 'https://jmstechsupport.com.au/assets/autoposter/tech/review-tom-m.jpg',
        'category': 'customer-proof', 'alt_text': 'Five-star Google review from Tom M. about a security camera installation and after-care.',
        'review_source': 'review-provenance.json#38',
    },
    {
        'rotation_index': '39', 'publish_order': 23.5,
        'title': 'Five-star review: a massive internet-speed difference',
        'caption': 'A recent five-star Google review after slow-internet troubleshooting.\n\n"By the time he left, my internet was so much faster. The difference was massive."\n\nSlow internet is not something you have to put up with. JMS Tech Support can diagnose Wi-Fi and home-network problems across the Clarence Valley.',
        'image_path': str(assets / 'review-mekala-h.jpg'), 'image_filename': 'review-mekala-h.jpg',
        'image_url': 'https://jmstechsupport.com.au/assets/autoposter/tech/review-mekala-h.jpg',
        'category': 'customer-proof', 'alt_text': 'Five-star Google review from Mekala H. about troubleshooting slow internet.',
        'review_source': 'review-provenance.json#39',
    },
    {
        'rotation_index': '40', 'publish_order': 30.5,
        'title': 'Five-star review: reliability matters',
        'caption': 'A recent five-star Google review.\n\n"Josh was very professional, he knew what he was talking about. Each time he turned up when he said he would."\n\nStraight answers, practical help and a technician who turns up. JMS Tech Support comes to you across Yamba, Maclean and the Clarence Valley.',
        'image_path': str(assets / 'review-wendi-m.jpg'), 'image_filename': 'review-wendi-m.jpg',
        'image_url': 'https://jmstechsupport.com.au/assets/autoposter/tech/review-wendi-m.jpg',
        'category': 'customer-proof', 'alt_text': 'Five-star Google review from Wendi M. about professionalism and reliability.',
        'review_source': 'review-provenance.json#40',
    },
    {
        'rotation_index': '41', 'publish_order': 36.5,
        'title': 'Five-star review: cameras with after-care',
        'caption': 'A recent five-star Google review after a security camera installation.\n\n"Great service great products and great after service"\n\nA security camera install should not end when the hardware goes up. JMS Tech Support provides practical setup and after-care across the Clarence Valley.',
        'image_path': str(assets / 'review-wendy-d.jpg'), 'image_filename': 'review-wendy-d.jpg',
        'image_url': 'https://jmstechsupport.com.au/assets/autoposter/tech/review-wendy-d.jpg',
        'category': 'customer-proof', 'alt_text': 'Five-star Google review from Wendy D. about security cameras, products and after-care.',
        'review_source': 'review-provenance.json#41',
    },
    {
        'rotation_index': '42', 'publish_order': 8.5,
        'title': 'Five-star review: peace of mind from an external camera',
        'caption': 'A recent five-star Google review after an external security camera installation.\n\n"Very happy with my external camera, great peace of mind"\n\nIf you want practical security-camera advice without the sales routine, JMS Tech Support comes to you across Yamba, Maclean and the Clarence Valley.',
        'image_path': str(assets / 'review-helen-b.jpg'), 'image_filename': 'review-helen-b.jpg',
        'image_url': 'https://jmstechsupport.com.au/assets/autoposter/tech/review-helen-b.jpg',
        'category': 'customer-proof', 'alt_text': 'Five-star Google review from Helen B. about an external security camera and peace of mind.',
        'review_source': 'review-provenance.json#42',
    },
]

plan = json.loads(plan_path.read_text())
state = json.loads(brand_state_path.read_text())
old_items = sorted(plan['rotation'], key=lambda value: float(value.get('publish_order', value['rotation_index'])))
next_key = old_items[int(state['cursor'])]['rotation_index']
existing_keys = {item['rotation_index'] for item in plan['rotation']}
new_reviews = [item for item in reviews if item['rotation_index'] not in existing_keys]
if new_reviews:
    shutil.copy2(plan_path, plan_path.with_suffix('.json.pre-reviews.bak'))
    shutil.copy2(brand_state_path, brand_state_path.with_suffix('.json.pre-reviews.bak'))
    plan['rotation'].extend(new_reviews)
    ordered = sorted(plan['rotation'], key=lambda value: float(value.get('publish_order', value['rotation_index'])))
    state['cursor'] = next(index for index, item in enumerate(ordered) if item['rotation_index'] == next_key)
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n')
    brand_state_path.write_text(json.dumps(state, indent=2) + '\n')
print({'added_keys': [item['rotation_index'] for item in new_reviews], 'next_key_preserved': next_key, 'new_cursor': state['cursor']})
