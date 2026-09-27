# فصل ۱۵ — ۱۵ سوال مرورگر، DOM و تله‌های JS با جواب کامل

> 🎯 **هدف:** نیمه‌ی گمشده‌ی مصاحبه‌ها: DOM و مرورگر + سوالات «خروجی‌بگو». از سوالات واقعی [Front End Interview Handbook](https://frontendinterviewhandbook.com/javascript-questions/) و [کوییز JavaScript Questions](https://github.com/lydiahallie/javascript-questions) (۱۴۰+ سوال معروف Lydia Hallie) انتخاب شده — **بدون تکرار فصل ۵**.

> 💡 سوالات «خروجی این کد چیست؟» را بلند حل کن: اول حدس، بعد توضیح، بعد اجرا — همان‌طور که در مصاحبه باید حرف بزنی.

---

## ۱۵.۱ — DOM و مرورگر

### Q1: سه فاز event چیست و event delegation چطور کار می‌کند؟

**جواب:** رویداد سه فاز دارد: **capturing** (از window به پایین) → **target** (المان واقعی) → **bubbling** (به بالا). delegation یعنی listener را روی والد گذاشتن و آیتم واقعی را از `event.target` پیدا کردن — یک listener به‌جای هزار تا، و روی آیتم‌های اضافه‌شده‌ی بعدی هم کار می‌کند:

```js
list.addEventListener("click", (e) => {
  const btn = e.target.closest("button.delete");
  if (!btn) return;                 // کلیک روی جای دیگرِ لیست
  removeItem(btn.dataset.id);       // 👈 delegation + data-* (فصل ۱۴ Q5)
});
```

**عمیق‌تر:** دو ابزار متفاوت که همیشه با هم اشتباه گرفته می‌شوند: `stopPropagation` جلوی بالا رفتن رویداد؛ `preventDefault` جلوی رفتار پیش‌فرض مرورگر (لینک، submit، کلید). و `event.target` = المان واقعی کلیک‌شده، `event.currentTarget` = المانی که listener رویش است. React هم ذاتاً delegate است (روی root — به همین دلیل React 17 به بالا attach به root است).

### Q2: فرق attribute و property در DOM؟

**جواب:** attribute چیزی است که در HTML نوشته‌ای (`<input value="x">`)؛ property فیلد زنده‌ی آبجکت DOM (`input.value`). کاربر تایپ می‌کند → property عوض می‌شود، attribute همان اولی می‌ماند.

**عمیق‌تر:** `getAttribute("value")` مقدار **اولیه** HTML را می‌دهد؛ `input.value` مقدار **فعلی**. برای checkbox هم: `checked` property رفت‌وبرگشت دارد، attribute فقط default است. در React/JSX این مرز را فریم‌ورک مدیریت می‌کند — ولی سوال پشت سوال همین است.

### Q3: فرق DOMContentLoaded و load؟

**جواب:** `DOMContentLoaded`: درخت DOM آماده است (منتظر تصویر/iframe نیست) — جای init های معمول؛ `load`: همه‌ی منابع هم رسیده‌اند — دیر. اسکریپت‌های `defer` (و ES Module ها) دقیقاً قبل از DOMContentLoaded اجرا می‌شوند (فصل ۱۴ Q3).

**عمیق‌تر:** در SPA معمولاً هیچ‌کدام را دستی نمی‌خواهی — mount شدن فریم‌ورک نقطه‌ی شروع توست؛ `load` برای کارهایی مثل خواندن ابعاد واقعی تصویر یا متریک‌ها.

### Q4: فرق cookie، sessionStorage و localStorage؟

**جواب:** cookie: ~۴KB، **با هر request به سرور می‌رود**، expiry دارد و فلگ‌های امنیتی (httpOnly/secure/SameSite)؛ localStorage: ~۵-۱۰MB، دائمی، فقط کلاینت؛ sessionStorage: مثل localStorage ولی تا بستن تب.

**عمیق‌تر:** جواب تصمیمی بده: توکن → cookie با httpOnly (JS نمی‌خواندش — ضد XSS)؛ سبد خرید/تنظیمات UI → localStorage؛ داده‌ی موقتِ تب → sessionStorage. نگه‌داشتن توکن در localStorage = سطح حمله‌ی XSS فعال (فصل ۷ Q15 امنیت Next).

### Q5: Same-Origin Policy و CORS چیست؟

**جواب:** SOP: JS یک origin فقط به origin خودش (پروتکل + دامنه + پورت) دسترسی دارد. **CORS مکانیزم استانداردِ استثناست**: سرور با هدر `Access-Control-Allow-Origin` اعلام می‌کند کدام origin مجاز است.

**عمیق‌تر:** درخواست‌های «غیرساده» (POST با JSON، هدر سفارشی) اول **preflight** با متد `OPTIONS` می‌فرستند و سرور باید همان route را جوابش را بدهد. نکته‌ی کلیدی: کلاینت نمی‌تواند CORS را دور بزند — خطای CORS یعنی درد **سرور** است؛ راه‌حل فرانت: پروکسی سمت سرور (در Next: Route Handler یا rewrites)، نه تغییر fetch!

---

## ۱۵.۲ — تله‌های JS (فرمت «خروجی بگو»)

### Q6: coercion — خروجی این‌ها؟

```js
function sum(a, b) { return a + b; }
sum(1, "2");     // "12"  — + با رشته یعنی چسباندن
3 + 4 + "5";     // "75"  — چپ‌به‌راست: (3+4)=7، بعد 7+"5"
"5" - 3;         // 2     — - فقط ریاضی است؛ "5" → number
+true;           // 1
[] + {};         // "[object Object]"
```

**چرا:** `+` دو کاره است — اگر یکی از عملوندها رشته باشد، چسباندن؛ `-` فقط عددی. تبدیل پیش‌فرض: `[] → ""` و `{} → "[object Object]"`. (پایه‌ی `==` از فصل ۵ Q2.)

### Q7: typeof و instanceof — خروجی‌ها؟

```js
typeof null;          // "object"   👈 باگ تاریخی؛ سازگاری! هرگز فیکس نمی‌شود
typeof NaN;           // "number"
typeof typeof 1;      // "string"   — typeof 1 === "number"، typeof آن "string"
new Number(3) === 3;  // false      — آبجکتِ wrapper ≠ primitive
3 instanceof Number;  // false      — primitive در سمت راست معنا ندارد
```

**عمیق‌تر:** چک عدد واقعی: `Number.isNaN(x)` (نه `x === NaN`)، چک آرایه: `Array.isArray`، و برای همه‌چیز: `Object.prototype.toString.call(x)`.

### Q8: falsy ها و ممیز شناور — خروجی؟

```js
!!null; !!""; !!" "; !!0; !!NaN; !![]; !!"0";
// false  false  true  false  false  true  true
0.1 + 0.2 === 0.3;  // false → 0.1 + 0.2 = 0.30000000000000004
```

**چرا:** شش falsy: `false, 0, "", null, undefined, NaN` — پس `" "` و `[]` و `"0"` truthy اند! ممیز شناور: مقایسه با آستانه — `Math.abs(a - b) < Number.EPSILON` — یا گرد کردن با `toFixed`.

### Q9: کدام متدهای آرایه mutate می‌کنند؟ slice/splice؟

```js
const a = [1, 2, 3, 4, 5];
a.slice(1, 3);       // [2, 3]      — کپی؛ a سالم
const b = [1, 2, 3, 4, 5];
b.splice(1, 3);      // [2, 3, 4]   — برش زد؛ b حالا [1, 5]
const c = [1];
c.push(6);           // 2           — push طولِ جدید برمی‌گرداند، نه آرایه!
[10, 1, 2].sort();   // [1, 10, 2]  — مقایسه‌ی رشته‌ای!
```

**چرا:** mutating ها: `push/pop/shift/unshift/splice/sort/reverse/fill` — بقیه (`map/filter/slice/concat`) کپی می‌سازند. sort عددی: `(a, b) => a - b`. در React هرگز mutate نکن — state جدید بساز (snapshot فصل ۶ Q5).

### Q10: forEach یا map؟

**جواب:** `map` آرایه‌ی جدید با **خروجی** callback می‌سازد؛ `forEach` فقط پیمایش می‌کند و برنمی‌گرداند (undefined).

**تله (دو خطای واقعی کد ریویو):**

```js
arr.map((x) => console.log(x));   // [undefined, undefined, ...] — forEach می‌خواست!
const names = await Promise.all(  // async داخل map فقط Promise می‌سازد
  ids.map(async (id) => getUser(id))
);                                // 👈 با Promise.all جمع کن
```

### Q11: for...in و for...of؟

```js
const arr = ["a", "b"];
for (const x in arr) console.log(x);  // "0", "1" — کلیدها (index به‌صورت رشته)!
for (const x of arr) console.log(x);  // "a", "b" — مقادیر
```

**چرا:** `for...in` روی **enumerable keys** می‌چرخد (حتی میراث پروتوتایپ — فصل ۵ Q8)؛ `for...of` روی **iterables** (Array، String، Map، Set). برای آبجکت معمولی: `Object.entries(obj)` + `for...of` یا `Object.keys/values`.

### Q12: this گمشده — خروجی؟

```js
const circle = {
  radius: 10,
  diameter() { return this.radius * 2; },
  perimeter: () => this.radius * 2 * Math.PI,  // 👈 arrow داخل آبجکت!
};
circle.diameter();   // 20
circle.perimeter();  // NaN — this آررو از enclosing می‌آید → undefined
const d = circle.diameter;
d();                 // NaN (sloppy) یا TypeError (strict) — this از دست رفت
```

**چرا:** arrow `this` خودش ندارد (lexical — فصل ۵ Q6)؛ و متدِ جدا شده از آبجکت هم `this` را می‌بازد — راه‌حل: `bind` (فصل ۵ Q7) یا گرفتن متد داخل تابع دیگر.

### Q13: زنجیره‌ی Promise — خروجی؟

```js
Promise.resolve(1)
  .then((x) => x + 1)                  // 2
  .then((x) => { throw x; })           // پرش به نزدیک‌ترین catch
  .catch(() => 3)                      // 3 — زنجیره ادامه پیدا می‌کند
  .then((x) => x * 10)                 // 30
  .finally(() => console.log("done"))  // "done" — ولی مقدار را عوض نمی‌کند
  .then((x) => console.log(x));        // 30
```

**چرا:** هر `then` خروجی قبلی را می‌گیرد؛ `throw` تا نزدیک‌ترین `catch` می‌پرد؛ catch اگر مقدار برگرداند زنجیره «سالم» ادامه می‌یابد؛ `finally` pass-through است. (تکمیل async/await فصل ۵ Q10.)

### Q14: const و Object.freeze — این کد چه می‌کند؟

```js
const user = { name: "M", tags: ["a"] };
user.name = "M2";      // ✅ مجاز — const فقط بازتخصیص را می‌بندد، نه تغییر را
Object.freeze(user);
user.name = "M3";      // بی‌صدا بی‌اثر (در strict: TypeError)
user.tags.push("b");   // 😱 انجام می‌شود! freeze سطحی است
```

**چرا:** `freeze` فقط properties سطح اول را قفل می‌کند؛ آبجکت‌های تودرتو هنوز مرجع مشترک‌اند (ریشه‌ی مشترک با shallow/deep copy فصل ۵ Q12). deep freeze دستی/کتابخانه‌ای است — و پاس مصاحبه: «برای immutability واقعی در state، خودم کپی می‌سازم».

### Q15: ASI — چرا خروجی undefined است؟

```js
function get() {
  return
  {
    ok: true,
  };
}
get();  // undefined — return همان‌جا تمام شد؛ آبجکت هرگز ساخته نشد!
```

**چرا:** Automatic Semicolon Insertion بعد از `return/throw/break/continue/new` پایان خط می‌گذارد؛ براکتِ خط بعد statement جدا و مرده است. قاعده: باز کردن پرانتز/براکت روی همان خط — به همین دلیل JSX چندخطی را `return (` می‌نویسی و Prettier هم همین را الزام می‌کند. (نکته strict: حالت strict بی‌صداها را ارور می‌کند — مثل تخصیص متغیر بدون تعریف.)

---

## ✅ جمع‌بندی فصل

- DOM: delegation = یک listener برای همه؛ `target ≠ currentTarget`؛ جلوگیری از انتشار (stopPropagation) ≠ جلوگیری از رفتار پیش‌فرض (preventDefault)
- مرورگر: توکن → httpOnly cookie؛ خطای CORS = درد سرور؛ DOMContentLoaded جای init
- تله‌ها: `+` با رشته می‌چسباند، `typeof null`، sort رشته‌ای، forEach بدون return، freeze سطحی، ASI بعد return
- منابع این فصل: سوالات واقعی هندبوک فرانت + کوییز ۱۴۰ سوالی Lydia Hallie — خودت را با آن بزن: **روزی ۵ سوال، حدس بزن بعد اجرا**

## 📝 تمرین فصل ۱۵

1. پنج سوال از [کوییز JavaScript Questions](https://github.com/lydiahallie/javascript-questions) را انتخاب کن: بدون اجرا حدس بزن، بعد اجرا — و برای هر اشتباه، «چرا» را یک جمله بنویس.
2. لیست TODO فصل ۸ را با delegation بازنویسی: یک listener روی `<ul>`، حذف/تیک با `data-*`.
3. در پروژه‌ای که fetch بین‌دامنه‌ای دارد، یک بار عمداً CORS را بشکن و بعد با Route Handler پروکسی‌اش کن — تجربه‌ی واقعی برای جواب Q5.
4. خروجی این را حدس بزن و اجرا کن:

```js
const user = { name: "Ali", tags: ["x"] };
Object.freeze(user);
user.tags[0] = "y";
console.log(user.tags[0]);
```

<details><summary>جواب تمرین ۴</summary>

`"y"` — freeze فقط سطح اول را قفل می‌کند؛ آرایه‌ی داخل آبجکت هنوز mutable است. برای قفل کامل باید بازگشتی همه‌ی سطوح را freeze کنی (deep freeze).
</details>

➡️ **بعدش کجاست؟** برگرد به [فصل ۱۳](./13-cheatsheet.md) — چیت‌شیت و چک‌لیست‌ها را با این ۳۵ سوال تازه تمرین کن، بعد سراغ مصاحبه‌های واقعی برو.
