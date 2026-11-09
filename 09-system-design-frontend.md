# فصل ۹ — System Design برای فرانت‌کار: با پاسخ نمونه کامل

> 🎯 **هدف:** «یک کامپوننت X را طراحی کن» یا «فرانت یک فروشگاه را طراحی کن» — ترسناک به نظر می‌رسد چون ساختار جواب ندارد. این فصل قالب ۵ مرحله‌ای + دو پاسخ نمونه کامل می‌دهد.

---

## ۹.۱ — قالب ۵ مرحله‌ای پاسخ (حفظ کن!)

```text
۱. شفاف‌سازی (Requirements):      ۲-۳ سوال بپرس — کاربران؟ داده؟ مقیاس؟ آفلاین؟
۲. تعریف دامنه (Scope):           چیزهای داخل و خارج دامنه را صریح بگو
۳. معماری کلی:                    نقشه بلوک‌ها (صفحات، لایه‌ها، سرویس‌ها) — روی صفحه بکش
۴. عمق‌کاوی جزئیات:               state، کش، پرفورمنس، ارور، دسترسی‌پذیری
۵. Trade-off ها و توسعه آینده:   «اگر X شد، این‌جوری scale می‌کنم»
```

> 💡 نکته طلایی: مصاحبه‌گر **طرح درستِ واحد** را نمی‌خواهد — می‌خواهد ببیند سوال می‌پرسی، trade-off می‌بینی و تصمیم‌ها را دلیل می‌آوری. سوال نپرسیدن و مستقیم کد نوشتن = پرچم قرمز بزرگ‌ترین.

---

## ۹.۲ — پاسخ نمونه ۱: «یک Autocomplete/جستجوی زنده طراحی کن»

**مرحله ۱ — شفاف‌سازی (بلند بگو):**
- «نتایج از سرور می‌آید یا لیست لوکال؟» — (فرض: سرور)
- «چند کاربر همزمان؟ سرعت API؟» — (فرض: API تا 200ms)
- «موارد لازم: debounce؟ keyboard navigation؟ اخیراً جستجوها؟» — (فرض: بله همه)

**مرحله ۲ — Scope:** «شامل: input، dropdown نتایج، keyboard nav، highlight متن، loading و empty state. خارج از دامنه: صفحه نتیجه کامل، analytics.»

**مرحله ۳ — معماری:**

```text
SearchBox (کلاینت — state دار)
├── Input (uncontrolled + debounce 300ms)
├── useSearch(query) hook
│   ├── AbortController — لغو درخواست قبلی
│   └── cache ساده در Map برای query های تکراری
└── Results dropdown
    ├── Skeleton حین لود
    ├── keyboard: ↑↓ Enter Esc (roving focus)
    └── aria: role="listbox" / aria-activedescendant
```

**مرحله ۴ — عمق‌کاوی:**

- **Race condition:** پاسخ حرف «a» دیرتر از «ab» برسد؟ → AbortController + چک رشته درخواست با آخرین query
- **پرفورمنس:** debounce ۳۰۰ms + حداقل ۲ حرف + AbortController؛ نتایج ≤ ۱۰
- **State:** query → URL نه state (shareable)؛ selected index → useState؛ نتایج → از hook
- **a11y:** listbox/option، label برای input، focus مدیریت
- **ارور:** پیام «نتایج نیامد، دوباره تلاش کن» + retry — نه خاموشی

**مرحله ۵ — Trade-off و آینده:** «برای داده لوکال، فیلتر سمت کلاینت با useMemo کافی بود — سرور برای داده بزرگ و خصوصی. آینده: highlight با `<mark>`، تاریخچه در localStorage، SSR نتیجه اولیه.»

---

## ۹.۳ — پاسخ نمونه ۲: «فرانت‌اند یک فروشگاه آنلاین را طراحی کن»

**مرحله ۱ — شفاف‌سازی:** «تعداد محصول؟ ترافیک؟ سئو مهم است؟ (بله!) تیم بک‌اند چه API ای می‌دهد؟ ادمین جدا است؟»

**مرحله ۲ — Scope:** داخل: لیست/جزئیات محصول، سبد، checkout، جستجو. خارج: پرداخت واقعی (با درگاه)، ادمین.

**مرحله ۳ — معماری (این را بکش):**

```text
Next.js App Router
├── / (لیست)          ISR + revalidateTag("products")
├── /product/[slug]   ISR + generateStaticParams + generateMetadata (سئو!)
├── /cart             Client Component (state لوکال/Context) + localStorage sync
├── /checkout         Server Actions → درگاه → webhook تأیید
├── /api/webhooks/payment   Route Handler (idempotent!)
└── auth              session cookie (httpOnly)
داده: Product → از DB با tags؛ تصاویر → next/image + remotePatterns
```

**مرحله ۴ — عمق‌کاوی:**

- **سئو:** صفحات محصول ISR + metadata داینامیک + sitemap از DB — جستجوی گوگل حیات کسب‌وکار است
- **سبد خرید:** state کلاینتی (Context کوچک) + همگام با localStorage؛ بعد از لاگین با سرور sync؛ قیمت‌ها همیشه از سرور (امنیت!)
- **پرفورمنس:** لیست = ISR؛ تصاویر next/image با sizes؛ فیلترها با searchParams (shareable)؛ جزئیات کند → استریم ریویوها با Suspense
- **پرداخت:** Server Action → درگاه؛ webhook با idempotency key (دوباره زدن = دوبار شارژ نشود!)؛ خطا → پیام و retry
- **ارور و حالت‌ها:** empty state، out-of-stock، خطای درگاه با retry
- **a11y:** فرم‌ها با label، تمرکز مدیریت‌شده، کنتراست

**مرحله ۵ — Trade-off و آینده:** «ISR سرعت را می‌دهد ولی تازگی قیمت را ۶۰ ثانیه دیر — برای قیمت لحظه‌ای، fetch بدون کش در بخش قیمت جزئیات. اگر ترافیک جهانی شد: i18n + CDN region. اگر سبد سنگین شد: microservice سبد جدا.»

---

## ۹.۴ — سوالات دنباله‌دار (که بعد از طرحت می‌پرسند!)

| سوال | الگوی جواب |
|---|---|
| «اگر ترافیک ۱۰× شد؟» | کش لایه‌ای (CDN/ISR) → read replica → صف‌ها → فقط بعداً microservice |
| «چطور تست می‌کنی؟» | واحد منطق + integration فرم‌ها + e2e مسیر خرید (Playwright) |
| «API کند شد چه می‌شود؟» | loading state، timeout + retry with backoff، skeleton، پیام صادقانه |
| «دسترسی‌پذیری؟» | semantic HTML، keyboard، aria، کنتراست — از ابتدا نه آخر پروژه |
| «کش را کی باطل می‌کنی؟» | mutation → revalidateTag؛ webhook از CMS/بک‌اند |

---

## ✅ جمع‌بندی فصل

- قالب ۵ مرحله: شفاف‌سازی → Scope → معماری (بکش!) → عمق‌کاوی → Trade-off
- سوال پرسیدن اول = قوی‌ترین سیگنال senior بودن
- عمق‌کاوی = state/کش/پرفورمنس/ارور/a11y — همین پنج‌تا را همیشه پوشش بده
- هر تصمیم با دلیل و «اگر X شد، Y می‌کنم»

## 📝 تمرین فصل ۹

1. دو پاسخ نمونه را **بلند** ارائه بده (ضبط کن) — هر کدام ۱۰-۱۵ دقیقه.
2. طراحی کن: «صفحه داشبورد ادمین با جدول داده بزرگ، فیلترها و Real-time» — با قالب ۵ مرحله.
3. طراحی کن: «سیستم کامنت‌گذاری با reply و لایک» — state، API، بهینه‌سازی.
4. برای پاسخ نمونه ۱، سه سوال شفاف‌سازی دیگر پیدا کن که نپرسیدم.

<details><summary>راهنمای تمرین ۲ (اسکلت پاسخ)</summary>

۱. شفاف‌سازی: چند ردیف؟ (۱۰هزار؟) فیلترها سمت سرور یا کلاینت؟ real-time چقدر جدی؟ صادرات اکسل؟
۲. معماری: جدول سروری (Server Component با پارامترهای URL) + فیلترها با searchParams + virtualization برای ردیف‌ها + تعامل bulk با client island + WebSocket/SSE فقط برای بخش real-time واقعی (نوتیف).
۳. عمق: pagination cursor (نه offset در این حجم) + index در DB بک‌اندی (پیشنهاد بده!) + skeleton + export در صف.
۴. Trade-off: همه‌چیز کلاینت راحت ولی کند و سنگین؛ همه‌چیز سروری امن و سریع ولی تعامل کند — ترکیب جزیره‌ای بهترین است.
</details>

➡️ **فصل بعد:** مصاحبه رفتاری — STAR با چهار جواب نمونه کامل.
