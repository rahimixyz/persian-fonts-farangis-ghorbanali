import sys
from PIL import Image, ImageDraw, ImageFont

font, out = sys.argv[1], sys.argv[2]
letters = sys.argv[3] if len(sys.argv) > 3 else 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئؤءآ'
size = 110
f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
Z = '‍'
cols = 4
cw, ch = 300, 260
rows_per = 2
items = []
for c in letters:
    items += [c, c + Z, Z + c + Z, Z + c]
n = len(items)
percol = 4 * 4  # 4 letters per row-band of 16 cells? keep simple grid of 16 columns
gc = 16
cw = 112 * 1.0
W = int(gc * 112 + 40)
rows = (n + gc - 1) // gc
H = rows * ch + 20
im = Image.new('L', (W, H), 255)
d = ImageDraw.Draw(im)
for i, t in enumerate(items):
    r, c = divmod(i, gc)
    x = W - 20 - c * 112 - 56
    y = 20 + r * ch + 150
    if i % 4 == 0:
        d.line([(x + 56, y - 150), (x + 56, y + 100)], fill=200)
    d.line([(x - 50, y), (x + 50, y)], fill=225)
    d.text((x, y), t, font=f, fill=0, direction='rtl', language='fa', anchor='ms')
im.save(out)
