#!/usr/bin/env python3
"""Turn site/img/designs/*.png (from tools/shots.js) into 640x400 .webp thumbnails.
The share card is made separately (img/share-card.jpg)."""
import json
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'site', 'img', 'designs')
home = json.load(open(os.path.join(ROOT, 'content', 'facts.json'))).get('home', 'brochure')
for f in sorted(os.listdir(D)):
    if not f.endswith('.png'):
        continue
    k = f[:-4]
    im = Image.open(os.path.join(D, f)).convert('RGB')
    im.resize((640, 400), Image.LANCZOS).save(os.path.join(D, k + '.webp'), 'WEBP', quality=82)
    os.remove(os.path.join(D, f))
print('thumbnails written to', D)
