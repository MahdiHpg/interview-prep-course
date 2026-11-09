# فصل ۱۴ — ۲۰ سوال HTML/CSS با جواب کامل

> 🎯 **هدف:** بزرگ‌ترین شکاف مصاحبه‌های فرانت بعد از JS: سوالات HTML و CSS. این فصل از سوالات واقعی [Front End Interview Handbook](https://github.com/yangshun/front-end-interview-handbook) (مجموعه‌ی معروف h5bp) استخراج شده و **هیچ هم‌پوشانی با فصل‌های ۵-۷ ندارد**. هر سوال: جواب کوتاه + نکته عمیق.

> 💡 سوالات HTML/CSS معمولاً «گرم‌کننده» اول مصاحبه‌اند — جواب سریع و مطمئن در این بخش، لحن کل مصاحبه را تعیین می‌کند.

---

## ۱۴.۱ — HTML

### Q1: Semantic HTML چیست و چرا مهم است؟

**جواب:** استفاده از تگ‌های معنادار (`header`، `nav`، `main`، `article`، `section`، `footer`، `figure`) به‌جای div-soup؛ مرورگر و اسکرین‌ریدر «معنا» را می‌فهمند، نه فقط شکل.

**عمیق‌تر:** سه برنده دارد: دسترسی‌پذیری (پیمایش با landmark ها)، سئو (خزنده ساختار را می‌فهمد) و خودت (خوانایی کد). تست ساده: صفحه بدون CSS هنوز باید قابل‌فهم باشد.

### Q2: DOCTYPE چه می‌کند؟

**جواب:** به مرورگر اعلام می‌کند سند را در **standards mode** رندر کند. بدون آن (یا با doctype ناقص قدیمی) مرورگر به **quirks mode** می‌رود: box model قدیمی و رفتارهای ناسازگار بین مرورگرها.

**عمیق‌تر:** `<!DOCTYPE html>` همین و فقط همین. برای چک کردن mode فعال: `document.compatMode` → `"CSS1Compat"` یعنی standards.

### Q3: فرق `<script>`، `<script async>` و `<script defer>`؟

**جواب:** هر سه دانلودشان همزمان با پارس HTML شروع می‌شود؛ فرق در **اجرا** است:

| حالت | کی اجرا می‌شود؟ | ترتیب |
|---|---|---|
| `<script>` | فوری بعد از دانلود — پارس HTML را بلاک می‌کند | به‌ترتیب سند |
| `async` | هر وقت دانلود تمام شد | نامعلوم! |
| `defer` | بعد از پارس کامل، درست قبل DOMContentLoaded | به‌ترتیب سند |

**عمیق‌تر:** اسکریپت مستقل (analytics) → `async`؛ اسکریپت‌های وابسته به DOM و به‌هم → `defer`. ES Module ها به‌طور پیش‌فرض رفتار defer دارند — و دیگر لازم نیست script را آخر body بگذاری (سوال بعدی).

### Q4: چرا CSS را در head و script را (قدیم‌ها) آخر body می‌گذاشتند؟

**جواب:** CSS در head تا اولین رندر استایل کامل داشته باشد (وگرنه **FOUC** — فلش محتوا بدون استایل)؛ script پایین صفحه تا پارس HTML بلاک نشود و کاربر زودتر محتوا ببیند.

**عمیق‌تر:** CSS رندر-بلاکینگ است (CSSOM باید آماده شود) و JS پارس-بلاکینگ. جایگزین مدرن script پایین صفحه همان `defer` در head است — و در Next.js کل این چیدمان را فریم‌ورک مدیریت می‌کند (فصل ۷). ایده‌ی «بخش‌بخش فرستادن صفحه» همان است که امروز streaming می‌نامیم (فصل ۷ Q6).

### Q5: attribute های `data-*` به چه دردی می‌خورند؟

**جواب:** جای استاندارد چسباندن داده‌ی سفارشی به المان: `data-product-id="42"` — خواندن با `el.dataset.productId` (خط‌ها camelCase می‌شوند).

**عمیق‌تر:** کاربردهای واقعی: سلکتور تست (`data-testid` در Testing Library)، state کوچک UI، و event delegation (فصل بعد Q1). تله: داده‌ای که به React باید برسد در state/props است — `data-*` برای کد خارج از ری‌اکت است.

### Q6: صفحه‌ی چندزبانه چطور می‌سازی؟

**جواب:** `lang` درست روی `<html>` (مثلاً `fa`)، `dir="rtl"` برای راست‌به‌چپ، `hreflang` روی `<link>` برای معرفی نسخه‌های زبانی به موتور جستجو، و آدرس مجزا برای هر زبان (مسیر یا زیردامنه).

**عمیق‌تر:** نکته‌های طراحی چندزبانه: طول متن‌ها فرق دارد (آلمانی ~۳۰٪ بلندتر) — layout را با flex/grid انعطاف‌پذیر بگیر، نه عرض ثابت؛ فونت و line-height مخصوص هر اسکریپت؛ تاریخ/عدد با `Intl`. برای فارسی: فونت وزیرمتن + دقت در `dir` که متن مخلوط (اعداد/انگلیسی داخل فارسی) به‌هم نریزد.

### Q7: `srcset` در `<img>` چه می‌کند و مرورگر چطور انتخاب می‌کند؟

**جواب:** چند فایل با عرض‌های مختلف پیشنهاد می‌دهی و با `sizes` اعلام می‌کنی تصویر در viewport من چند پیکسل جا می‌گیرد؛ مرورگر با **DPR** و عرض واقعی، بهترین گزینه را خودش برمی‌دارد:

```html
<img
  src="hero-1024.jpg"
  srcset="hero-480.jpg 480w, hero-1024.jpg 1024w, hero-2048.jpg 2048w"
  sizes="(max-width: 600px) 480px, 800px"
  width="1024" height="512" loading="lazy" alt="..."
/>
```

**عمیق‌تر:** `width/height` صریح = CLS صفر؛ `loading="lazy"` = دانلود وقتی نزدیک viewport. در Next همه‌ی این‌ها را `next/image` خودکار می‌کند (فصل ۷ Q13) — ولی در پروژه‌های بدون فریم‌ورک، srcset سوال رایج است.

---

## ۱۴.۲ — CSS

### Q8: box model را توضیح بده؛ `* { box-sizing: border-box }` چه می‌کند؟

**جواب:** هر المان = content + padding + border + margin. پیش‌فرض `content-box` است: `width` فقط content را می‌شمارد؛ با `border-box`، عرض شامل padding و border هم می‌شود — محاسبه‌ی layout انسانی می‌شود.

**عمیق‌تر:** تقریباً همه‌ی reset های مدرن (و Bootstrap) با border-box شروع می‌کنند. فرق **reset** (همه‌چیز را صفر می‌کند) و **normalize** (پیش‌فرض‌های مفید را حفظ و فقط ناسازگاری‌ها را یکسان می‌کند) را هم یک جمله بلد باش.

### Q9: Specificity چطور محاسبه می‌شود؟ `!important` کی؟

**جواب:** وزن سه‌رقمی: **(id، class/attribute/pseudo-class، element)** — مثلاً `#nav .link` با (1,1,0) از `a:hover` با (0,1,1) می‌چربد. مساوی بودن؟ ترتیب سورس: آخرین می‌برد. `!important` از همه بالاتر است.

**عمیق‌تر:** مرورگر سلکتور را **از راست به چپ** مچ می‌کند (اول آخرین بخش را چک می‌کند — ارزان‌ترین). ترفند مدرن: `:where(#id, .class)` specificity صفر می‌دهد — برای reset های ایمن. جواب مصاحبه‌ای `!important`: «برای غلبه بر استایل ابزار بیرونی (مثل override کردن بوت‌استرپ) رایج است، ولی مسیر درست اول specificity درست است — important آخرین راه‌حل.»

### Q10: block، inline و inline-block چه فرقی دارند؟

**جواب:** `block` تمام عرض خط را می‌گیرد و width/height می‌پذیرد؛ `inline` در جریان متن می‌ماند و width/height **نمی‌پذیرد**؛ `inline-block` در جریان متن است ولی ابعاد می‌پذیرد — ابزار کلاسیک badge و دکمه‌ی کوچک.

**عمیق‌تر:** تله‌ی کلاسیک inline: vertical padding پس‌زمینه را رنگ می‌کند ولی layout نمی‌زند (روی خط مجاور می‌ریزد). مدرن: با flex/grid کمتر به inline-block نیاز داری؛ `inline-flex` برای آیتم درون‌متنیِ فلکسی.

### Q11: مقادیر position را توضیح بده؟

**جواب:** `static` (پیش‌فرض)؛ `relative` از جای عادی جابجا می‌شود و **مرجع absolute فرزندانش** است؛ `absolute` نسبت به نزدیک‌ترین جدِ non-static؛ `fixed` نسبت به viewport؛ `sticky` ترکیب relative+fixed — تا رسیدن به آستانه عادی، بعد چسبیده.

**عمیق‌تر:** تله‌های fixed: جدی که `transform/filter/perspective` دارد مرجع آن می‌شود و «fixed بودن» می‌شکند. `sticky` به `overflow: hidden` در جد حساس است (اسکرول کانتینر می‌شود). کاربرد sticky: هدر جدول و sidebar.

### Q12: Flexbox یا Grid؟

**جواب:** flex برای **یک‌بعدی** (toolbar، ردیف کارت، بین‌فاصله‌ها)؛ grid برای **دوبعدی** (layout صفحه، گالری با ستون‌های منظم). ترکیب درست: صفحه با grid، داخل هر ناحیه flex.

**عمیق‌تر:** flex محتوا-محور است (اندازه از محتوا می‌آید)، grid طرح-محور (شبکه تعریف می‌کنی). سوال دنباله: `justify-content` روی محور اصلی، `align-items` روی محور عرضی — و با `flex-direction` جایشان عوض می‌شود؛ `flex: 1` یعنی `grow:1 shrink:1 basis:0`.

### Q13: یک باکس را دقیقاً وسط والدش چطور می‌گذاری؟ (سه روش)

**جواب:**

```css
/* ۱) flex */           .parent { display: flex; justify-content: center; align-items: center; }
/* ۲) grid — کوتاه‌ترین */ .parent { display: grid; place-items: center; }
/* ۳) کلاسیک */          .child { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
```

**عمیق‌تر:** روش absolute برای مرکزکردن روی یک المان دیگر (tooltip) لازم است — و استفاده از translate به‌جای top/left یعنی بدون reflow (سوال Q18).

### Q14: z-index چرا کار نمی‌کند؟ (stacking context)

**جواب:** z-index فقط در همان **stacking context** معنا دارد. هر المانی با position non-static + z-index، یا `opacity < 1`، `transform`، `filter` و... یک context جدید می‌سازد — z-index فرزندش فقط داخل همان محدوده مقایسه می‌شود.

**عمیق‌تر:** باگ کلاسیک: مودال با z-index ۹۹۹۸ داخل والدی با transform — زیر مودالی می‌ماند که بیرون آن با z-index ۱۰ است. راه‌حل: context ها را تخت نگه دار و مقیاس سراسری z-index (مثلاً 100/200/300) تعریف کن. همین‌جا BFC را هم بگو: `overflow: hidden` یک BFC می‌سازد که float را محاصره و margin-collapse را قطع می‌کند — ابزار کلاسیک clearing.

### Q15: چطور عنصری را مخفی کنم؟ (سه راه + sr-only)

**جواب:** `display: none` — از layout و درخت دسترسی‌پذیری حذف؛ `visibility: hidden` — جایش را نگه می‌دارد ولی نامرئی و غیرقابل‌تعامل؛ `opacity: 0` — نامرئی ولی **قابل‌تعامل و focus**! برای «فقط screen reader»: کلاس sr-only (absolute، 1px، clip).

**عمیق‌تر:** تله: `opacity: 0` روی input یعنی کاربر با tab می‌رسد و «چیزی که نیست» را تعامل می‌کند. اگر transition می‌خواهی، `visibility` را با تأخیر داخل transition ترکیب کن.

### Q16: فرق pseudo-class و pseudo-element؟

**جواب:** pseudo-class **وضعیت** المان را هدف می‌گیرد (`:hover`، `:focus-visible`، `:nth-child()`)؛ pseudo-element **بخشی از المان** را می‌سازد (`::before`، `::after`، `::placeholder`، `::selection`) — با خاصیت `content`.

**عمیق‌تر:** `::before/::after` برای دکور بدون DOM اضافه (خط، badge، آیکون)؛ `:focus-visible` به‌جای `:focus` تا کلیک موس outline نگیرد ولی کیبورد بگیرد. فرم صحیح pseudo-element های جدید: دو نقطه (`::`).

### Q17: mobile-first یعنی چه؟ responsive و adaptive چه فرقی دارند؟

**جواب:** mobile-first یعنی CSS پایه برای موبایل نوشته شود و با `min-width` به سمت صفحه‌های بزرگ‌تر توسعه یابد. responsive: یک layout که با viewport انعطاف می‌گیرد؛ adaptive: نسخه‌های ثابت جدا برای هر breakpoint (مرسوم نیست).

**عمیق‌تر:** سوال چرخشی هندبوک: «@media غیر از screen؟» → `@media print` (استایل چاپ رزومه/فاکتور). و در grid های مدرن، `repeat(auto-fit, minmax(240px, 1fr))` جای چندین media query را می‌گیرد.

### Q18: چرا برای انیمیشن از `translate()` به‌جای `top/left`؟

**جواب:** `top/left` تغییر layout می‌دهد (reflow + paint)؛ `transform` بعد از layout عمل می‌کند و فقط paint/composite می‌گیرد (GPU) — انیمیشن‌های 60fps با `transform` و `opacity` ساخته می‌شوند، نه خواص layout.

**عمیق‌تر:** این پل به فصل بعد است: reflow گران‌ترین مرحله pipeline رندر است (فصل ۱۵ Q6). ابزار دیدن: DevTools → Rendering → Paint flashing.

### Q19: تم تاریک را با CSS چطور می‌سازی؟

**جواب:** متغیرهای CSS روی `:root` تعریف و زیر `[data-theme="dark"]` بازتعریف می‌شوند؛ کامپوننت‌ها فقط `var(--color-bg)` می‌خوانند؛ سوییچ‌کننده attribute را عوض می‌کند (با next-themes و `attribute="data-theme"`).

```css
:root { --color-bg: #fff; --color-ink: #111; }
[data-theme="dark"] { --color-bg: #0f172a; --color-ink: #e2e8f0; }
.card { background: var(--color-bg); color: var(--color-ink); }
```

**عمیق‌تر:** preprocessor (Sass) روزی برای nesting و mixin بود؛ امروز nesting بومی CSS و متغیرها اکثر نیازها را پوشش می‌دهند. `color-scheme: light dark` را هم اعلام کن تا فرم‌ها و اسکرول‌بار سیستم هماهنگ شوند.

### Q20: فونت سفارشی چطور لود کنی که متن فلش نزند؟

**جواب:** با `font-display`: `swap` (فوراً فونت جایگزین، بعد تعویض) یا `optional` (اگر نرسید اصلاً تعویض نکن)؛ با `preload` دانلود را زودتر شروع کن؛ فقط وزن‌های لازم را ساب‌ست کن.

**عمیق‌تر:** دو اصطلاح را بلد باش: **FOUT** (فلش متن بدون استایل) و **FOIT** (متن نامرئی تا رسیدن فونت — بدترین). در Next همه‌چیز حل‌شده است: `next/font` فونت را self-host و preload می‌کند و layout shift صفر می‌دهد (فصل ۷ Q16).

---

## ✅ جمع‌بندی فصل

- HTML: معنایی بنویس، `defer` بگذار، ابعاد تصویر را صریح بده، `lang/dir` را فراموش نکن
- CSS: border-box، specificity سه‌رقمی، flex یک‌بعدی / grid دوبعدی، انیمیشن فقط transform/opacity
- تله‌های پرتکرار: z-index و stacking context، sticky و overflow، opacity:0 قابل‌تعامل، FOUT/FOIT فونت
- منبع این فصل: سوالات واقعی Front End Interview Handbook (h5bp) — بدون تکرار فصل‌های ۵-۷

## 📝 تمرین فصل ۱۴

1. Specificity را حدس بزن بدون اجرا: کدام می‌برد؟ `#nav .link` / `.nav .link:hover` / `ul li a.active` — بعد در DevTools (پنل Styles، strike-through شده‌ها) چک کن.
2. صفحه‌ای با یک باکس بساز و هر سه روش وسط‌چین (Q13) را عملی پیاده کن.
3. جدولی با هدر sticky بساز (Q11) — و بعد `overflow: hidden` روی والد بگذار تا شکستن sticky را ببینی.
4. کلاس `sr-only` را بدون کپی بنویس (Q15) — و با یک screen reader مرورگر تستش کن.
5. تم تاریک با `data-theme` + متغیرها بساز (Q19) — سه رنگ، دو تم.

<details><summary>جواب تمرین ۱</summary>

`#nav .link` با (1,1,0) از همه بالاتر است (`.nav .link:hover` = (0,3,0)، `ul li a.active` = (0,1,3)). اگر دو سلکتور هم‌وزن بودند، ترتیب سورس تصمیم می‌گرفت. `!important` از همه این‌ها بالاتر می‌پرید.
</details>

➡️ **فصل بعد:** ۱۵ سوال مرورگر، DOM و تله‌های JS — نیمه‌ی گمشده‌ی دیگر مصاحبه.
