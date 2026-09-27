# فصل ۶ — ۲۰ سوال React با جواب کامل

> 🎯 **هدف:** میدان اصلی مصاحبه‌ی فرانت‌اند تو. هر سوال: جواب مصاحبه‌ای + نکته عمیق. از فصل ۱-۴ مرور Next هم پشتیبانی می‌کنیم (چون سوال‌ها گاهی React خالص، گاهی در Next).

---

## ۶.۱ — مبانی

### Q1: Virtual DOM چیست و چرا؟

**جواب:** React یک نمایش سبک DOM را در حافظه نگه می‌دارد؛ هنگام تغییر state، درخت جدید با قبلی مقایسه می‌شود (reconciliation/diffing) و فقط قسمت‌های تغییرکرده به DOM واقعی اعمال می‌شوند — چون دستکاری DOM گران‌ترین عملیات مرورگر است.

**عمیق‌تر:** الگوریتم O(n) با فرض‌های React: عناصر هم‌نوع مقایسه می‌شوند؛ key ها هویت آیتم‌های لیست را می‌دهند.

### Q2: رندر و re-render کی رخ می‌دهد؟

**جواب:** رندر = صدا زدن تابع کامپوننت. re-render وقتی: state عوض شود، والد re-render شود (بدون memo)، یا context مصرفی تغییر کند.

**نکته:** re-render یعنی اجرای دوباره تابع — نه لزوماً تغییر DOM (diff بعدش تصمیم می‌گیرد). StrictMode دو بار صدا می‌زند برای کشف ناخالصی.

### Q3: چرا key و چرا index بد است؟

**جواب:** key هویت آیتم را بین رندرها به React می‌دهد تا diff درست انجام شود. index وقتی لیست reorder/insert می‌شود، آیتم اشتباه را به key قبلی می‌چسباند → state داخلی آیتم‌ها (input ها!) جابجا می‌شود و diff ناکارآمد می‌شود.

### Q4: props drilling چیست و راه‌حل‌ها؟

**جواب:** پاس دادن props از لایه‌های واسط بی‌استفاده. راه‌حل‌ها به ترتیب: composition (children — معمولاً کافی است!) → Context (برای داده کم‌تغییر سراسری) → ابزار state سراسری (Zustand/TanStack) برای state سروری.

---

## ۶.۲ — State و Effects

### Q5: useState و snapshot semantics؟

**جواب:** state در هر رندر یک snapshot ثابت است؛ آپدیت وابسته به مقدار قبلی → فرم تابعی `setX(x => x+1)`؛ چند setState در یک event batch می‌شود. (فصل ۲ مرور Next کاملش را دارد.)

### Q6: useEffect دقیقاً برای چیست و چه چیزهایی نیست؟

**جواب:** همگام‌سازی با سیستم‌های بیرونی (subscription، DOM غیرری‌اکتی، تایمر) — با cleanup. نیست: محاسبه مشتق‌شده (در رندر)، event handling (در handler)، fetch داده در اپ‌های جدی (فریم‌ورک/Query).

**نکته:** وابستگی‌ها صادقانه؛ cleanup قبل هر اجرای دوباره؛ race condition با ignore flag یا AbortController.

### Q7: useMemo/useCallback کی؟

**جواب:** `useMemo` محاسبه سنگین یا مرجع پایدار برای وابستگی؛ `useCallback` خود تابع برای memoized children یا dependency. بدون اندازه‌گیری نزن — React Compiler در راه است.

### Q8: فرق controlled و uncontrolled component؟

**جواب:** controlled: value از state می‌آید (single source of truth — onChange => setState)؛ uncontrolled: DOM خودش نگه می‌دارد و با ref می‌خوانی (مثلاً `<input defaultValue>` یا file input).

**انتخاب:** فرم ساده/فایل → uncontrolled سبک‌تر؛ اعتبارسنجی زنده/شرط‌ها → controlled. (در Next.js فرم‌ها با Server Action هم می‌روند.)

### Q9: Context چه وقت anti-pattern است؟

**جواب:** برای state پرتغییر پرتکرار (مثل مقدار input) — هر تغییر همه‌ی مصرف‌کننده‌ها را re-render می‌کند. راه: state را نزدیک مصرف‌کننده نگه دار، Context را به چند Context کوچک بشکن، یا state سروری را با Query مدیریت کن.

---

## ۶.۳ — معماری و پرفورمنس

### Q10: React.memo و کامپوننت‌ها؟

**جواب:** `memo(Component)` رندر مجدد را وقتی props بدون تغییرند حذف می‌کند — فقط وقتی: رندر سنگین است + والدش زیاد re-render می‌شود + props پایدار پاس می‌دهند (پس useCallback/useMemo همراهش لازم است). سه شرط باهم، وگرنه بی‌فایده.

### Q11: key-based reset؟

**جواب:** ترفند مستند: برای reset کامل یک کامپوننت (فرم!)، به آن `key={resetCounter}` بده — تغییر key = unmount/remount و همه state اول می‌شود. تمیزتر از reset کردن ده state دستی.

### Q12: lifting state در برابر state سراسری؟

**جواب:** اول lifting (نزدیک‌ترین جد مشترک)؛ اگر درخت عمیق شد composition؛ اگر سروری است و چند صفحه دارد → TanStack Query (cache + retry + stale logic آماده)؛ client-side سراسری واقعی (تم/سشن) → Context/Zustand.

### Q13: error boundary چیست؟

**جواب:** کامپوننتی که ارورهای رندر فرزندان را می‌گیرد (در React با componentDidCatch/useEffect+throw در Next از error.tsx استفاده می‌کنی) — از فاجعه‌ی «سفیدشدن کل اپ» جلوگیری می‌کند و بخش خطادیده را ایزوله می‌کند. ارورهای event handler را نمی‌گیرد (try/catch دستی).

### Q14: Suspense چه می‌کند؟

**جواب:** به کامپوننت‌های «معلق» (promise که با use خوانده می‌شود، یا lazy) یک fallback می‌دهد — رندر بدون بلاک ادامه می‌یابد و وقتی آماده شد جایگزین می‌شود. در Next.js با streaming همان است (فصل ۹ مرور).

---

## ۶.۴ — React 19 و مدرن

### Q15: React 19 چه چیزهای جدیدی آورد؟

**جواب:** هوک‌های فرم (useActionState/useFormStatus/useOptimistic)، هوک `use` (خواندن promise/context با شرط)، ref به عنوان prop معمولی ( goodbye forwardRef)، بهبود پیام‌های hydration، و پایه‌ی Server Components/Actions (که در Next مصرف می‌کنیم).

### Q16: Server Component چیست و فرقش با SSR کلاسیک؟

**جواب:** SSR کلاسیک فقط رندر اولیه HTML بود و بعد کل JS می‌آمد hydrate شود. Server Component کدی است که **فقط روی سرور اجرا می‌شود** و payload رندرشده می‌فرستد — JS آن هرگز به کلاینت نمی‌رود؛ می‌تواند مستقیم دیتابیس بخواند. Client Component ها (use client) برای interactivity هستند و در سرور هم pre-render می‌شوند.

### Q17: چرا key در لیست ولی در فرم هم می‌گذارند؟

**جواب (سوال چرخشی):** همان منطق هویت — برای «force remount» یک کامپوننت (مثلاً خالی کردن فرم بعد از submit) `key={version}` عوض می‌کنی تا React آن را از نو بسازد؛ تمیزتر از دستی صفر کردن ۱۰ state.

### Q18: چطور یک لیست بزرگ ۱۰هزار آیتمی را رندر می‌کنی؟

**جواب:** virtualization — فقط آیتم‌های داخل viewport رندر می‌شوند (react-window / TanStack Virtual)؛ همراه memo روی ردیف‌ها. اگر داده از سرور است: pagination/cursor + infinite scroll. هرگز ۱۰هزار DOM node نریز.

### Q19: StrictMode چه می‌کند و چرا دو بار رندر؟

**جواب:** در dev، دوبار صدا زدن کامپوننت‌ها/effects برای لو رفتن side-effect ها و ناخالصی. production حذف است. دیدن دوباره‌ی لاگ‌ها باگ نیست — سیگنال اصلاح است.

### Q20: state را کجا نگه داری: URL، useState، سرور؟

**جواب (سوال سطح بالا):** فیلترها و صفحه‌ها → URL (searchParams — shareable و back-safe)؛ UI موقت (modal باز) → useState؛ داده‌ی سرور → TanStack Query یا fetch در Server Component (فصل ۷ مرور Next). هر داده یک خانه‌ی درست دارد — duplicating state را حذف کن.

---

## ✅ جمع‌بندی فصل

- هسته: VDOM/reconciliation، key، snapshot، effects همگام‌ساز
- پرفورمنس: memo سه‌شرطی، virtualization، Context ضدالگو
- React 19: فرم‌هوک‌ها، use، Server Components
- هر جواب + «در پروژه‌ی من...» = امتیاز

## 📝 تمرین فصل ۶

1. ده سوال از این فصل را انتخاب و با ضبط صدا جواب بده (هر کدام زیر ۶۰ ثانیه).
2. Q18 را عملی کن: یک لیست ۵۰۰۰ آیتمی بساز، بدون virtualization benchmark بگیر، بعد با virtualization — اعداد را یادداشت کن (در مصاحبه عدد طلایی است!).
3. سوال چرخشی Q13 را آماده کن: «error boundary در Next.js چطور؟» → error.tsx (فصل ۹ مرور).
4. مصاحبه‌گر می‌گوید «useEffect را دوست ندارم» — منظورش چیست و جوابت؟ (راهنما: You Might Not Need an Effect)

<details><summary>جواب نمونه تمرین ۴</summary>

یعنی با استفاده‌های اشتباه effect جنگیده (محاسبه در effect، event در effect، chain های fetch). جوابت: «موافقم — اکثر useEffect هایی که می‌بینم جای دیگری belong می‌کنند: محاسبه در رندر، رویداد در handler، و fetch سروری در Server Component. Effect را من فقط برای همگام‌سازی بیرونی نگه می‌دارم — subscription ها و ...» + یک مثال refactor واقعی از پروژه‌ات.
</details>

➡️ **فصل بعد:** ۱۶ سوال Next.js — خانه دوم تو.
