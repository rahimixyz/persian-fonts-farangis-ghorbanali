# Persian fonts: Farangis & Ghorbanali — فونت‌های فارسی فرنگیس و قربانعلی

**[فارسی](#فارسی)** · **[English](#english)** · [صفحهٔ نمایش و آزمایش فونت](index.html) · [تغییرات](CHANGELOG.md)

<div dir="rtl">

## فارسی

دو فونت فارسی رایگان و متن‌باز از **علیرضا رحیمی**.

| فونت | کاربرد | وزن‌ها | فرمت‌ها |
|---|---|---|---|
| **قربانعلی** (Ghorbanali) | متن وب‌سایت، اپلیکیشن و رابط کاربری | ۶ وزن: نازک ۳۰۰، معمولی ۴۰۰، متوسط ۵۰۰، نیم‌ضخیم ۶۰۰، ضخیم ۷۰۰، خیلی ضخیم ۸۰۰ | WOFF2، WOFF، TTF، OTF |
| **فرنگیس** (Farangis) | تیتر، بنر، بیلبورد، پوستر، تابلوی بزرگراه | ۵ وزن: متوسط ۵۰۰، نیم‌ضخیم ۶۰۰، ضخیم ۷۰۰، خیلی ضخیم ۸۰۰، سیاه ۹۰۰ | WOFF2، WOFF، TTF، OTF |

![قربانعلی](specimens/ghorbanali.png)

![فرنگیس](specimens/farangis.png)

### سریع‌ترین راه: یک خط در HTML

بدون دانلود و بدون نصب؛ در هر سایتی کار می‌کند، چه HTML ساده، چه وردپرس، لاراول، جنگو یا ری‌اکت:

</div>

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rahimixyz/persian-fonts-farangis-ghorbanali@main/fonts.css">
<style>
  body { font-family: "Ghorbanali", Tahoma, sans-serif; }
  h1, .banner { font-family: "Farangis", "Ghorbanali", sans-serif; font-weight: 900; }
</style>
```

<div dir="rtl">

همهٔ وزن‌ها در CSS تعریف شده‌اند؛ کافی است `font-weight` را عوض کنید (مثلاً `font-weight: 500`). فاصلهٔ خطوط در همهٔ وزن‌های یک خانواده یکسان است، پس تغییر وزن متن را جابه‌جا نمی‌کند.

فقط یکی از دو فونت را می‌خواهید؟ به‌جای `fonts.css` از `Ghorbanali/ghorbanali.css` یا `Farangis/farangis.css` استفاده کنید.

### استفاده در هر محیط

| محیط | روش |
|---|---|
| **HTML / هر سایت** | همان یک خط `<link>` بالا. یا پوشهٔ فونت را کنار فایل‌های سایت بگذارید و `ghorbanali.css` را لینک کنید. |
| **وردپرس** | در «نمایش ← سفارشی‌سازی ← CSS اضافی» بنویسید: `@import url("https://cdn.jsdelivr.net/gh/rahimixyz/persian-fonts-farangis-ghorbanali@main/fonts.css");` و بعد `body { font-family: "Ghorbanali"; }` |
| **PHP / لاراول** | خط `<link>` را در `resources/views/layouts/app.blade.php` داخل `<head>` بگذارید. برای میزبانی روی سرور خودتان، پوشهٔ `Ghorbanali` را در `public/fonts` کپی کنید و `{{ asset('fonts/Ghorbanali/ghorbanali.css') }}` را لینک کنید. |
| **React / Next.js / Vue** | خط `<link>` را در `index.html` یا `app/layout` بگذارید، یا فایل‌های `woff2` را در `public/fonts` کپی کنید. در Next.js می‌توانید از `next/font/local` با فایل‌های `woff2` استفاده کنید. |
| **پایتون** (تصویر و نمودار) | Pillow: `ImageFont.truetype("Ghorbanali-Regular.ttf", 32, layout_engine=ImageFont.Layout.RAQM)` · matplotlib: `font_manager.fontManager.addfont("Ghorbanali-Regular.ttf")` و بعد `rcParams["font.family"] = "Ghorbanali"` |
| **اندروید** | فایل `ttf` را در `res/font/` بگذارید و `android:fontFamily="@font/ghorbanali_regular"` |
| **iOS** | فایل `ttf` را به پروژه اضافه کنید، در `Info.plist` زیر `UIAppFonts` بنویسید و `UIFont(name: "Ghorbanali-Regular", size: 17)` |
| **فلاتر** | در `pubspec.yaml` زیر `fonts:` فایل‌های `ttf` را معرفی کنید و `fontFamily: 'Ghorbanali'` |
| **فتوشاپ، ایلاستریتور، فیگما، ورد، کنوا** | فایل‌های `otf` یا `ttf` را دانلود و روی سیستم نصب کنید. |

### دانلود

فایل‌ها در پوشه‌های [`Ghorbanali/fonts`](Ghorbanali/fonts) و [`Farangis/fonts`](Farangis/fonts) هستند و هر فرمت پوشهٔ جداگانه دارد:
* `woff2`: بهترین برای وب، کوچک‌ترین حجم
* `woff`: برای مرورگرهای قدیمی
* `ttf`: برای اپلیکیشن، پایتون و نصب روی سیستم
* `otf`: برای نرم‌افزارهای طراحی

### پوشش نویسه‌ها

* همهٔ ۳۲ حرف فارسی با شکل‌های آغازی، میانی، پایانی و تنها؛ ترکیب «لا»؛ همزه و حروف همزه‌دار؛ ي، ك، ى و ة عربی
* ارقام فارسی و عربی (۰ تا ۹) و **ارقام لاتین (0 تا 9)** با ارتفاع یکسان
* علائم: ، ؛ ؟ ? ! . : « » ( ) [ ] - – — ٪ % ٫ ٬ + = / \ | * # < > ~ _ … • ×
* اعراب، نیم‌فاصله و کشیده؛ اعراب ترکیبی (مثل تشدید با فتحه) روی هم می‌نشینند و با هم برخورد نمی‌کنند
* کرنینگ: فاصلهٔ حروفی که به هم نمی‌چسبند (مثل «را»، «ورود»، «زن») به‌صورت خودکار و نوری تنظیم شده است
* حروف لاتین (A تا Z) را ندارند؛ برای متن انگلیسی یک فونت لاتین در `font-family` بگذارید.

### آزمون خودکار

هر تغییر در این مخزن به‌طور خودکار ساخته و بررسی می‌شود (`src/audit.py`):
* هیچ نویسهٔ رایج فارسی جا نیفتاده باشد.
* هر حرف در جمله‌های واقعی شکل اتصالی درست را بگیرد؛ این بررسی بر اساس جدول رسمی اتصال یونیکد انجام می‌شود.
* محل اتصال حروف فاصله یا شکاف نداشته باشد.
* هیچ بخشی از حروف بیرون از کادر خط بریده نشود.
* اندازهٔ بدنهٔ حروف و فاصله‌ها در محدودهٔ فونت‌های وب استاندارد باشد.
* اعراب ترکیبی در کلمات نمونه با هم برخورد نکنند.

### مجوز

[SIL Open Font License 1.1](OFL.txt). استفاده در پروژه‌های شخصی و تجاری، از جمله چاپ، وب، اپلیکیشن و ویدیو، آزاد و رایگان است. فروش خود فایل فونت مجاز نیست و نسخهٔ تغییریافته باید نام دیگری داشته باشد. © ۲۰۲۶ علیرضا رحیمی

</div>

---

## English

**Free Persian (Farsi) fonts by Alireza Rahimi.** Open source, free for personal and commercial use (SIL Open Font License 1.1).

| Font | Best for | Style | Weights | Formats |
|---|---|---|---|---|
| **Ghorbanali** | Websites, apps, UI, body text | Rounded monoline sans, open counters, hinted for screens | Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800 | WOFF2, WOFF, TTF, OTF |
| **Farangis** | Banners, billboards, posters, highway & street signage, headlines, logos | Geometric Kufi display, sharp corners, square dots | Medium 500, SemiBold 600, Bold 700, ExtraBold 800, Black 900 | WOFF2, WOFF, TTF, OTF |

### Use from a CDN (any website, no download)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rahimixyz/persian-fonts-farangis-ghorbanali@main/fonts.css">
<style>
  body { font-family: "Ghorbanali", system-ui, sans-serif; }
  h1   { font-family: "Farangis", sans-serif; font-weight: 900; }
</style>
```

Single family: `Ghorbanali/ghorbanali.css` or `Farangis/farangis.css`.

### Use anywhere else

- **WordPress:** Customizer → Additional CSS → `@import url("https://cdn.jsdelivr.net/gh/rahimixyz/persian-fonts-farangis-ghorbanali@main/fonts.css");`
- **PHP / Laravel / Symfony:** put the `<link>` in your layout's `<head>`, or copy the `Ghorbanali` folder to `public/fonts` and link `ghorbanali.css`.
- **React / Next.js / Vue / Svelte:** `<link>` in `index.html` / root layout, or `next/font/local` with the `woff2` files.
- **Python:** Pillow `ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)`; matplotlib `font_manager.fontManager.addfont(path)`.
- **Android** `res/font/`, **iOS** `UIAppFonts`, **Flutter** `pubspec.yaml` `fonts:` — use the `ttf` files.
- **Desktop / design apps** (Photoshop, Illustrator, Figma, Office, Canva): install the `otf` or `ttf` files.

### Coverage

Full Persian alphabet with contextual forms (isolated, initial, medial, final), lam-alef ligatures, Arabic-letter variants (ي ك ى ة), hamza forms, Persian/Arabic-Indic digits and Latin digits 0–9 at matching height, Persian and ASCII punctuation, harakat with mark positioning, ZWNJ and tatweel. Shaping uses standard OpenType features (`init`, `medi`, `fina`, `rlig`, `mark`, `mkmk`, `kern`). Kerning is optical and automatic for letters that meet without joining. All weights of a family share the same line metrics. Latin letters are not included — pair with a Latin font.

### Build and test

Every glyph is generated from code (`src/letters.py`, centre-line skeletons → outlines with Shapely → fontTools).

```bash
pip install -r requirements.txt
python3 src/build.py .     # builds Farangis/fonts and Ghorbanali/fonts (ttf, otf, woff, woff2)
python3 src/audit.py       # coverage, contextual forms vs Unicode joining types, join gaps, metrics, spacing
python3 src/specimens.py   # specimen images
```

The audit runs on every push (`.github/workflows/fonts.yml`).

Keywords: Persian font, Farsi font, free Persian font, Persian web font, Farsi webfont, Persian display font, Persian Kufi font, billboard font, signage font, Iranian font, RTL font, Arabic-script font, فونت فارسی، فونت رایگان فارسی، فونت وب فارسی، فونت تیتر، فونت بنر، فونت کوفی.
