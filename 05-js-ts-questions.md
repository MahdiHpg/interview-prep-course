# فصل ۵ — ۱۸ سوال JavaScript/TypeScript با جواب کامل

> 🎯 **هدف:** پرتکرارترین سوالات JS/TS مصاحبه‌های فرانت — هر سوال: جواب کوتاه (۱۵ ثانیه‌ای) + نکته عمیق (وقتی بیشتر بخواهند). **تمرین: جواب‌ها را بلند بگو، نه بخوان.**

> 💡 الگوی جواب‌دهی: اول تعریف در یک جمله، بعد یک مثال یک‌خطی، بعد (اگر پرسیدند) trade-off.

---

## ۵.۱ — مبانی

### Q1: فرق var، let و const؟

**جواب کوتاه:** `var` function-scoped و hoisted است (undefined قبل از تعریف) و می‌تواند دوباره تعریف شود. `let` و `const` block-scoped اند و TDZ دارند. `const` بازتخصیص ممنوع (ولی محتوای آبجکتش تغییر می‌کند).

**نکته عمیق:** در کد مدرن تقریباً همیشه `const` مگر بازتخصیص لازم — و `var` عملاً منسوخ است. سوال پشت سوال معمولاً: «hoisting چیست؟» → بالا آمدن تعریف به ابتدای scope در فاز کامپایل.

### Q2: فرق `==` و `===`؟

**جواب کوتاه:** `==` قبل مقایسه type coercion می‌کند (`"1" == 1` → true)، `===` هم نوع هم مقدار را چک می‌کند.

**نکته عمیق:** دو استثنای معروف `==`: `null == undefined` → true و `NaN == NaN` → false (NaN با خودش برابر نیست!). قاعده: همیشه `===` مگر knowingly با null/undefined.

### Q3: Event Loop چیست؟ (پرسوالی‌ترین سوال JS!)

**جواب کوتاه:** JS single-threaded است؛ event loop صف callback ها (macrotask ها مثل setTimeout) و microtask ها (Promise ها) را می‌چرخد: کد sync تمام می‌شود → همه microtask ها → سپس یک macrotask → دوباره microtask ها...

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
// خروجی: 1 4 3 2   ← microtask (3) قبل از macrotask (2)!
```

**نکته عمیق:** این است که `setTimeout(fn, 0)` فوری نیست — فقط «در صف بعدی macrotask». و چرا رندر UI گیر نمی‌کند وقتی درست بنویسی.

### Q4: Closure چیست؟ مثال کاربردی؟

**جواب کوتاه:** تابعی که به متغیرهای scope پدرش — حتی بعد از پایان آن scope — دسترسی دارد.

```js
function makeCounter() {
  let count = 0;                 // private! از بیرون دسترسی نیست
  return () => ++count;
}
const inc = makeCounter();
inc(); inc(); // 2 — count زنده مانده است
```

**کاربردهای واقعی:** state خصوصی، debounce/throttle (تایمر داخل closure)، memoization. و تله معروفش در حلقه‌ها با `var` (همه همان count را می‌بینند؛ با `let` حل می‌شود).

### Q5: Hoisting و TDZ؟

**جواب کوتاه:** تعریف‌ها (declarations) قبل اجرا به بالای scope منتقل می‌شوند. Function declaration ها کامل hoist می‌شوند؛ `var` فقط تعریفش (undefined)؛ `let/const` hoist می‌شوند اما تا خط تعریف در TDZ (Temporal Dead Zone) اند و دسترسی ارور ReferenceError می‌دهد.

---

## ۵.۲ — توابع و this

### Q6: فرق arrow function و regular function؟

**جواب کوتاه:** سه فرق: arrow `this` خودش را ندارد (lexical — از enclosing می‌گیرد)، سازنده نیست (new نمی‌شود)، و `arguments` ندارد.

**نکته عمیق:** در event handler های کلاس قدیمی arrow لازم بود چون this را حفظ کند؛ در React مدرن با function component ها کمتر داغ است ولی در سوال ادامه دارد.

### Q7: call، apply و bind؟

**جواب کوتاه:** هر سه `this` را کنترل می‌کنند: `call(fn, thisArg, a, b)` آرگومان‌ها پشت هم؛ `apply` آرایه‌ای؛ `bind` نسخه‌ی جدیدِ بایندشده برمی‌گرداند (اجرا نمی‌کند).

**مثال:** `const log = console.log.bind(console)` — الگوی کلاسیک.

### Q8: Prototype و inheritance؟

**جواب کوتاه:** هر آبجکت JS یک `[[Prototype]]` دارد؛ جستجوی property اگر پیدا نشود به پروتوتایپ پدر می‌رود و بالاتر (prototype chain) تا null. کلاس‌های ES6 شیرین‌سازی همین مکانیزم‌اند.

**مثال کلاسیک:** `const arr = []; arr.map(...)` — `map` در `Array.prototype` است، نه خود arr.

---

## ۵.۳ — Async

### Q9: Promise و state هایش؟

**جواب کوتاه:** آبجکتی نماینده‌ی نتیجه‌ی آینده‌ی عملیات async — سه state دارد: pending → fulfilled / rejected (و یک‌بار برای همیشه قفل می‌شود). با `.then/.catch/.finally` یا `async/await` مصرف می‌شود.

### Q10: async/await چطور کار می‌کند؟ error handling؟

**جواب کوتاه:** `async` تابعی که همیشه Promise برمی‌گرداند؛ `await` توقف منطقی تا resolve (بدون بلاک کردن thread — زیر hood همان Promise chain است). خطا با try/catch گرفته می‌شود.

```js
async function load() {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);  // fetch روی 404 throw نمی‌کند!
    return await res.json();
  } catch (e) { /* شبکه یا http */ }
}
```

**نکته عمیق:** `await Promise.all([a, b])` برای اجرای موازی — سریالی await کردن دو fetch = waterfall (فصل ۷ مرور Next هم بود!).

### Q11: Promise.all در برابر allSettled و race؟

**جواب کوتاه:** `all` = همه موفق یا اولین reject (fail-fast)؛ `allSettled` = همه را منتظر می‌ماند و نتیجه هرکدام را جدا می‌دهد؛ `race` = اولین settle (موفق یا شکست)؛ `any` = اولین موفق.

**کاربرد واقعی:** لیست چند API مستقل → allSettled (یکی fail شد بقیه را نشان بده)؛ timeout دستی → race با تایمر.

---

## ۵.۴ — ساختار داده و الگوها

### Q12: فرق shallow و deep copy؟

**جواب کوتاه:** shallow فقط سطح اول را کپی می‌کند (`{...obj}`) — آبجکت‌های تودرتو هنوز مرجع مشترک دارند؛ deep copy کل درخت را (`structuredClone(obj)` استاندارد جدید).

**تله مصاحبه:** `{...user, address: {...user.address}}` — بدون دقت، تغییر `copy.address.city` اصل را هم عوض می‌کند!

### Q13: debounce و throttle؟ (پیاده‌سازی بخواهند!)

**جواب debounce:**

```js
function debounce(fn, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
```

**جواب throttle:**

```js
function throttle(fn, interval = 300) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= interval) {
      last = now;
      fn.apply(this, args);
    }
  };
}
```

**تفاوت:** debounce = «بعد از سکوت اجرا کن» (سرچ)؛ throttle = «حداکثر هر X ms یک بار» (اسکرول، resize). closure ها را که بلدی (Q4) هر دو را زنده می‌نویسی.

### Q14: map، filter، reduce — و reduce پیچیده؟

**جواب کوتاه:** map تبدیل، filter فیلتر، reduce تاخوردن به یک مقدار. reduce برای groupBy و tally:

```js
const byCat = items.reduce((acc, item) => {
  (acc[item.category] ??= []).push(item);
  return acc;
}, {});
```

**نکته:** `(acc[k] ??= [])` = «اگر نیست بساز» — با operator جدید `??=` خوش‌دست.

### Q15: فرق null و undefined؟ optional chaining و nullish؟

**جواب کوتاه:** undefined = «مقدار داده نشده» (سیستم)؛ null = «عمداً خالی» (برنامه‌نویس). `a?.b` = اگر a null/undefined نبود برو جلو؛ `a ?? b` = فقط برای null/undefined جایگزین کن (برخلاف `||` که 0 و "" را هم می‌گیرد!).

**تله کلاسیک:** `count || 10` وقتی count = 0 است → ۱۰! درست: `count ?? 10`.

---

## ۵.۵ — TypeScript

### Q16: type و interface چه فرقی دارند؟

**جواب کوتاه:** اکثراً همپوشان؛ interface قابلیت declaration merging دارد (تعریف دوباره = ادغام) و برای شکل آبجکت‌ها مرسوم است؛ type union/intersect/primitive ها و utility ها را هم می‌گیرد. قاعده تیم: یکی را انتخاب و یکدست کن.

### Q17: generic چیست و کجا به کار می‌آید؟

**جواب کوتاه:** تابع/نوعی که با type پارامتری می‌شود و تایپ‌سیف می‌ماند:

```ts
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
const n = first([1, 2]);      // n: number | undefined — خودکار!
```

**مثال واقعی:** `useActionState<TState, TFormData>` در React 19 — generics همه‌جا هستند.

### Q18: unknown و any و never؟

**جواب کوتاه:** `any` = چک تایپ خاموش (خطرناک)؛ `unknown` = همان انعطاف ولی مصرف‌کننده مجبور به narrow شدن است (امن)؛ `never` = هیچ مقداری (توابعی که همیشه throw یا حلقه بی‌نهایت) — برای exhaustiveness check هم کاربرد دارد.

**جمله طلایی:** «any را در کد production امضا نمی‌کنم — unknown بگیر و narrow کن.»

---

## ✅ جمع‌بندی فصل

- Event loop، closure، debonuce/throttle = سه سوال ستاره‌ی مصاحبه JS
- snapshot شدن state (فصل React) ریشه‌اش همین event loop و صف است
- `??` به جای `||` برای nullish واقعی؛ `unknown` به جای `any`
- هر جواب = یک جمله تعریف + مثال یک‌خطی + آمادگی برای سوال عمیق‌تر

## 📝 تمرین فصل ۵ (بلند بگو — ضبط کن!)

1. سه سوال Q1، Q3، Q9 را با ضبط صدا جواب بده و بشنو — کجاها گنگ است را اصلاح کن.
2. بدون نگاه به کتاب، debounce را بنویس (تایمر ۵ دقیقه) — بعد مقایسه کن.
3. خروجی این کد را حدس بزن، بعد اجرا کن:
```js
console.log("a");
setTimeout(() => console.log("b"));
Promise.resolve().then(() => console.log("c"));
console.log("d");
```
4. تابع `groupBy(items, keyFn)` با reduce بنویس و برای orders به تفکیک status تست کن.
5. تفاوت `obj.count || 5` و `obj.count ?? 5` را با سه مقدار count = 0، 5، undefined نشان بده.

<details><summary>جواب‌ها</summary>

3. خروجی: a d c b — sync اول (a, d)، بعد microtask (c)، بعد macrotask (b).
4. 
```ts
function groupBy<T>(items: T[], keyFn: (item: T) => string): Record<string, T[]> {
  return items.reduce((acc: Record<string, T[]>, item) => {
    const key = keyFn(item);
    (acc[key] ??= []).push(item);
    return acc;
  }, {});
}
```
5. count=0 → `||` می‌دهد ۵ (غلط!)، `??` می‌دهد ۰؛ count=5 → هر دو ۵؛ count=undefined → هر دو ۵.
</details>

➡️ **فصل بعد:** ۲۰ سوال React — میدان اصلی تو.
