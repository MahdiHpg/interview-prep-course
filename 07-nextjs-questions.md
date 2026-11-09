# فصل ۷ — ۱۶ سوال Next.js با جواب کامل

> 🎯 **هدف:** میدان تخصص تو — سوالاتی که برای موقعیت Next.js واقعاً پرسیده می‌شود (Next 15/16، App Router). هر سوال: جواب مصاحبه‌ای + عمیق‌تر. مرور فصل‌های ۵-۱۰ دوره Next پشتیبان این فصل است.

---

## ۷.۱ — App Router و رندر

### Q1: فرق App Router و Pages Router؟

**جواب:** App Router (پوشه app) با React Server Components بومی شده: پیش‌فرض سرور، layout های تو در تو با state پایدار، streaming/Suspense یکپارچه، Server Actions، و data fetching ساده با fetch/async. Pages Router (پوشه pages) مدل قدیمی getServerSideProps/getStaticProps است. پروژه‌های جدید: App Router.

### Q2: SSG، SSR، ISR — و کی هرکدام؟

**جواب:** SSG در build یک‌بار (لندینگ/مستندات)؛ ISR در build + بازتولید دوره‌ای (`revalidate = N` — بلاگ/فروشگاه)؛ SSR هر درخواست (داده شخصی/سشن). در App Router: پیش‌فرض static تا وقتی چیزی dynamic‌ش نکند (cookies/headers/searchParams/no-store).

### Q3: چطور یک صفحه را dynamic یا static نگه می‌داری؟

**جواب:** اعلام قصد: `revalidate` برای تازگی دوره‌ای؛ استفاده از `cookies()/headers()/searchParams` یا `fetch no-store` صفحه را dynamic می‌کند؛ `generateStaticParams` مسیرهای دینامیک را در build می‌سازد؛ و `dynamic = "force-dynamic"` برای اجبار.

### Q4: Server Component چیست و کی Client لازم است؟

**جواب:** پیش‌فرض سرور: کدش به کلاینت نمی‌رود، دیتابیس/secret مستقیم، async مستقیم. Client Component (`"use client"`) برای state/effect/رویداد/مرورگر API — و اولین رندرش هم SSR است. مرز یک‌طرفه به پایین است و داده فقط serializable رد می‌شود (تابع ممنوع به‌جز Server Actions).

### Q5: چرا params یک Promise است؟

**جواب (Next 15+):** برای سازگاری با استریم و async rendering — پارامترها ممکن است در آینده async حل شوند؛ پس `const { slug } = await params` (در کلاینت با `use(params)`).

### Q6: streaming چیست و چطور؟

**جواب:** HTML پوسته فوری ارسال و بخش‌های کند (کوئری سنگین) با `<Suspense>` بعداً تزریق می‌شوند — به جای بلاک شدن کل صفحه. `loading.tsx` همان Suspense خودکار مسیر است. TTFB و FCP عالی می‌شود.

### Q7: چرا این صفحه‌ام static نمی‌شود؟

**جواب (دیباگ رایج!):** یکی از این‌ها: `searchParams` خوانده شده، `cookies()/headers()`، fetch با no-store، یا random/Math.now در رندر. با `next build` ببین فلگ ○ (static) یا ƒ (dynamic) چیست — build گزارش هر مسیر را می‌دهد.

---

## ۷.۲ — داده و mutation

### Q8: Data fetching در App Router چطور انجام می‌شود؟

**جواب:** مستقیم `await fetch(...)` در Server Component (بدون useEffect!) با آپشن‌های کش (`next: { revalidate, tags }`)؛ Request Memoization یک URL را در یک رندر یک‌بار می‌زند؛ fetch های مستقل را `Promise.all` موازی کن (ضد waterfall)؛ داده کند را پایین‌تر ببر و استریم کن.

### Q9: Server Action چیست و چه فرقی با API Route دارد؟

**جواب:** تابع async با `"use server"` که کلاینت مستقیم صدا می‌زند (RPC) — برای فرم‌ها و mutation های UI خود سایت، با یکپارچگی فرم و progressive enhancement. Route Handler (`route.ts`) برای API عمومی: مصرف‌کننده خارجی، webhook، کنترل کامل هدر/status.

### Q10: بعد از mutation داده چطور تازه می‌شود؟

**جواب:** `revalidatePath("/blog")` یا `revalidateTag("posts")` داخل همان Server Action — کش مربوطه باطل و رندر بعدی تازه. جفتش با `fetch(..., { next: { tags: [...] } })`.

### Q11: how do you handle form validation? (فرم + اعتبارسنجی)

**جواب:** کلاینت: UX (فوری)؛ سرور: خط دفاع واقعی — zod در Server Action با `useActionState` برای برگرداندن ارور؛ هرگز به validation کلاینت اعتماد نکن؛ و authorization (صاحب رکورد) هم در همان اکشن.

### Q12: کجا داده state نگه می‌داری؟ (URL در برابر useState)

**جواب:** فیلتر/صفحه/تب → URL (searchParams — shareable، back-safe، SEO)؛ UI گذرا (مودال) → useState؛ داده سرور → fetch/Query. الگوی فیلتر: `router.push(?q=...)` و سرور رندر می‌کند.

---

## ۷.۳ — بهینه‌سازی و متادیتا

### Q13: next/image چه کار می‌کند و تنظیمات مهمش؟

**جواب:** resize/فرمت مدرن (WebP/AVIF) on-demand، lazy پیش‌فرض، CLS صفر (اجبار ابعاد)، `priority` برای LCP، `sizes` برای انتخاب منبع درست، `remotePatterns` برای دامنه‌های خارجی، `placeholder="blur"` با static import.

### Q14: Metadata و سئو در App Router؟

**جواب:** `export const metadata` استاتیک و `generateMetadata` داینامیک (از دیتابیس) — title template، openGraph، canonical. فایل‌های قراردادی: `sitemap.ts`، `robots.ts`، `opengraph-image.tsx` (OG با کد تولید می‌شود!). Yoast/دیتابیس → همان کوئری می‌شود metadata.

### Q15: چطور Next.js اپ را امن نگه می‌دارد و تو چه می‌کنی؟

**جواب:** Next: فرار خودکار خروجی، پشتیبانی CSP، Server Actions بدون endpoint عمومی، `NEXT_PUBLIC_` تنها راه لو دادن به باندل. من: رازها فقط سرور، validation سروری با zod، authorization در هر mutation، headers امنیتی در middleware/next.config.

### Q16: یک اپ Next.js را چطور بهینه برای Core Web Vitals می‌کنی؟

**جواب:** LCP: تصویر hero با priority + فونت با next/font (بدون درخواست خارجی) + استریم پوسته؛ CLS: ابعاد تصویر + skeleton؛ INP: جزایر کلاینت کوچک + transitions برای آپدیت‌های سنگین؛ داده: Promise.all + استریم؛ کش: ISR/revalidateTag درست.

---

## ✅ جمع‌بندی فصل

- رندر: static پیش‌فرض؛ قصد را اعلام کن (revalidate/no-store/cookies)
- داده: fetch سروری + memoization + Promise.all + streaming؛ mutation با Server Action + revalidateTag
- RSC: مرز serializable؛ params Promise؛ Client جزیره‌ای
- بهینه‌سازی: Image/Font/Metadata سه‌گانه Core Web Vitals

## 📝 تمرین فصل ۷

1. ۱۶ سوال را با ضبط صدا جواب بده — سوال‌های Q2، Q4، Q9، Q10 بیشترین فراوانی را دارند.
2. سناریو: مصاحبه‌گر می‌گوید «چرا Server Action به جای API معمولی برای فرم؟» — جوابت را با یک trade-off واقعی بده (بدون فصل ۸ مرور Next نگاه کن!).
3. «لیست محصولات ۱۰هزارتایی با فیلتر و جستجو» — معماری رندر و داده را طرح کن (SSG/ISR/SSR؟ URL؟ pagination؟).
4. از ریپوی یکی از پروژه‌هایت، `next build` بزن و گزارش static/dynamic هر مسیر را تفسیر کن.

<details><summary>جواب نمونه تمرین ۲ و ۳</summary>

تمرین ۲: «برای mutation های UI خود سایت، Server Action یک لایه RPC تایپ‌سیف بدون endpoint عمومی می‌دهد: فرم مستقیم به تابع وصل است، revalidateTag کنار ذخیره است و progressive enhancement هم دارد. اما برای مصرف‌کننده خارجی (اپ موبایل/webhook) Route Handler می‌سازم — اعتبارسنجی zod را مشترک نگه می‌دارم تا DRY باشد.»

تمرین ۳: لیست = ISR با revalidate ۶۰ و tags: ["products"]؛ فیلتر/جستجو با searchParams (dynamic) و cursor pagination؛ جزئیات = generateStaticParams برای محبوب‌ها + dynamicParams برای بقیه با ISR؛ mutation ادمین = Server Action + revalidateTag("products")؛ تصاویر next/image با remotePatterns.
</details>

➡️ **فصل بعد:** ۸ تمرین لایو-کدینگ با کد کامل.
