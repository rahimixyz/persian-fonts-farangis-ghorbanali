"""Render the same lines in several fonts, one block per font (visual regression aid)."""
import sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
size = int(sys.argv[2])
fonts = sys.argv[3:]
lines = [
    'فونت آرام و خوانا برای وب‌سایت‌ها',
    'می‌روم، خانه‌ها، کتاب‌ها، مسئولیت، نشانه‌گذاری',
    'اقامتگاه | بهترین قیمت | پشتیبانی ۲۴ ساعته',
    'زیباترین فصل برای عکاسی و طبیعت‌گردی',
    '۱۲۳۴۵۶۷۸۹۰ | 1234567890 | ۲۵۰٬۰۰۰ تومان (۱۴۰۵)',
]
lh = int(size * 1.8)
W = 1500
H = len(fonts) * (len(lines) * lh + 30)
im = Image.new('L', (W, H), 255)
d = ImageDraw.Draw(im)
y = 10
for fp in fonts:
    f = ImageFont.truetype(fp, size, layout_engine=ImageFont.Layout.RAQM)
    label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    d.text((10, y), fp.split('/')[-1], font=label, fill=120)
    for ln in lines:
        d.text((W - 20, y + int(size * 1.2)), ln, font=f, fill=0, direction='rtl', language='fa', anchor='rs')
        y += lh
    y += 30
    d.line([(0, y - 15), (W, y - 15)], fill=200)
im.save(out)
