"""Render specimen images into specimens/ (run from the repository root)."""
from PIL import Image, ImageDraw, ImageFont

R = ImageFont.Layout.RAQM
fb = 'Farangis/fonts/ttf/Farangis-Black.ttf'
fd = 'Farangis/fonts/ttf/Farangis-Bold.ttf'
gr = 'Ghorbanali/fonts/ttf/Ghorbanali-Regular.ttf'
gb = 'Ghorbanali/fonts/ttf/Ghorbanali-Bold.ttf'


def F(p, s):
    return ImageFont.truetype(p, s, layout_engine=R)


def t(d, xy, s, f, fill):
    d.text(xy, s, font=f, fill=fill, direction='rtl', language='fa', anchor='rs')


im = Image.new('RGB', (1600, 900), (20, 90, 60))
d = ImageDraw.Draw(im)
d.rectangle([40, 40, 1560, 860], outline=(255, 255, 255), width=10)
t(d, (1500, 230), 'فرنگیس', F(fb, 170), (255, 255, 255))
t(d, (1500, 430), 'خروجی شهرک غرب', F(fb, 120), (255, 255, 255))
t(d, (1500, 600), 'تخفیف ویژه ۵۰٪', F(fb, 120), (255, 214, 0))
t(d, (1500, 760), 'جشنواره بزرگ پاییزه — ۱۴۰۵', F(fd, 80), (255, 255, 255))
im.save('specimens/farangis.png')

im = Image.new('RGB', (1600, 900), (250, 248, 243))
d = ImageDraw.Draw(im)
t(d, (1520, 200), 'قربانعلی', F(gb, 140), (30, 30, 30))
t(d, (1520, 300), 'فونتی آرام و خوانا برای وب‌سایت‌ها', F(gr, 56), (90, 90, 90))
y = 430
for line in ['زبان فارسی یکی از زبان‌های کهن جهان است که امروز در ایران،',
             'افغانستان و تاجیکستان به آن سخن می‌گویند. این متن نمونه‌ای از',
             'حروف‌چینی با فونت قربانعلی در اندازهٔ متن بدنه است.']:
    t(d, (1520, y), line, F(gr, 44), (30, 30, 30))
    y += 80
t(d, (1520, 720), 'قیمت: ۱۲۵٬۰۰۰ تومان — «پیشنهاد ویژه»', F(gb, 48), (160, 60, 30))
t(d, (1520, 820), '۰۱۲۳۴۵۶۷۸۹  ،؛؟!«»()٪', F(gr, 48), (90, 90, 90))
im.save('specimens/ghorbanali.png')

for name, path in [('farangis-chars', fb), ('ghorbanali-chars', gr)]:
    im = Image.new('RGB', (1600, 620), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f = F(path, 84)
    for i, line in enumerate(['ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش', 'ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی',
                              'ء آ أ ؤ ئ ة لا ۀ ۰۱۲۳۴۵۶۷۸۹']):
        t(d, (1540, 140 + i * 190), line, f, (0, 0, 0))
    im.save('specimens/%s.png' % name)
