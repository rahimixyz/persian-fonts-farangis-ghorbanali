import sys
from PIL import Image, ImageDraw, ImageFont

font, out = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 90
lines = sys.argv[4:] or [
    'ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش',
    'ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی',
    'ببب ججج سسس صصص ططط ععع ففف ققق',
    'ککک گگگ للل ممم ننن ههه ییی لا ـلا',
    'سلام بر ایران، خانهٔ همیشگی ما!',
    'فرنگیس و قربانعلی ۱۲۳۴۵۶۷۸۹۰ ؟',
]
f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
W = 1800
lh = int(size * 1.75)
im = Image.new('L', (W, lh * len(lines) + 40), 255)
d = ImageDraw.Draw(im)
for i, l in enumerate(lines):
    y = 20 + i * lh + int(size * 1.0)
    d.line([(0, y), (W, y)], fill=225)
    d.text((W - 30, y), l, font=f, fill=0, direction='rtl', language='fa', anchor='rs')
im.save(out)
