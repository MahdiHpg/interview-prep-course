# فصل ۸ — ۸ تمرین Live Coding با کد کامل جواب

> 🎯 **هدف:** رایج‌ترین تمرین‌های زنده مصاحبه فرانت — هر تمرین: صورت مساله + نکات صحبت‌کردن + کد کامل. **با تایمر ۲۰ دقیقه تمرین کن و بلند حرف بزن.**

> 🗣️ **پروتکل طلایی لایو-کدینگ:**
> ۱. قبل از کد: سوال شفاف‌سازی بپرس («ورودی همیشه آرایه است؟ خالی ممکن است؟»)
> ۲. مسیر را بلند بگو («اول state، بعد fetch با loading، بعد...»)
> ۳. ساده شروع کن، بعد بهبود بده («نسخه ساده، بعداً virtualization»)
> ۴. حین کد: هر بلوک را یک جمله توضیح بده
> ۵. آخر: خودت با مثال تست کن و edge case بگو

---

## تمرین ۱ — Debounce Hook (پرتکرارترین!)

**صورت مساله:** «یک useDebounce بساز که ورودی جستجو با تاخیر ۳۰۰ms اعمال شود.»

```tsx
import { useEffect, useState } from "react";

function useDebouncedValue<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);   // هر تایپ جدید، تایمر قبلی را لغو می‌کند
  }, [value, delay]);

  return debounced;
}

// مصرف:
function Search() {
  const [query, setQuery] = useState("");
  const debounced = useDebouncedValue(query);

  useEffect(() => {
    if (debounced) fetchResults(debounced);
  }, [debounced]);
}
```

**بگو:** cleanup برای لغو تایمر قبلی — بدون آن هر تایپ یک fetch می‌سازد. و fetch هم race دارد (فصل ۳ مرور: ignore flag یا AbortController).

---

## تمرین ۲ — لیست با fetch و سه حالت

**صورت مساله:** «لیست کاربران از API با حالت‌های loading/error/empty/error.»

```tsx
function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [state, setState] = useState<"loading" | "error" | "ready">("loading");

  useEffect(() => {
    let ignore = false;
    fetch("/api/users")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => { if (!ignore) { setUsers(data); setState("ready"); } })
      .catch(() => { if (!ignore) setState("error"); });
    return () => { ignore = true };
  }, []);

  if (state === "loading") return <Skeleton />;
  if (state === "error") return <ErrorMessage onRetry={() => location.reload()} />;
  if (users.length === 0) return <EmptyState />;   // empty state را فراموش نکن!

  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

**بگو:** چهار حالت (loading/error/empty/ready) — اکثر کاندیداها سه‌تای اول را یادشان می‌رود. `ignore` برای race condition.

---

## تمرین ۳ — TODO List کامل

**صورت مساله:** «CRUD ساده: افزودن، تیک‌زدن، حذف، فیلتر.»

```tsx
type Todo = { id: number; text: string; done: boolean };

function Todos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<"all" | "active" | "done">("all");

  const add = (text: string) =>
    setTodos((t) => [...t, { id: Date.now(), text, done: false }]);   // فرم تابعی!
  const toggle = (id: number) =>
    setTodos((t) => t.map((x) => (x.id === id ? { ...x, done: !x.done } : x)));
  const remove = (id: number) => setTodos((t) => t.filter((x) => x.id !== id));

  const visible = todos.filter((t) =>
    filter === "all" ? true : filter === "done" ? t.done : !t.done
  );

  return (
    <>
      <AddForm onAdd={add} />
      <ul>{visible.map((t) => (
        <li key={t.id}>
          <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
          {t.text} <button onClick={() => remove(t.id)}>×</button>
        </li>
      ))}</ul>
      <FilterBar value={filter} onChange={setFilter} />
    </>
  );
}
```

**بگو:** immutable update (spread/map/filter)، فرم تابعی setState، و اینکه `visible` را محاسبه کردم نه state جدا (single source of truth).

---

## تمرین ۴ — Accordion

**صورت مساله:** «لیست سوالات FAQ — یکی باز، بقیه بسته؛ با کلیک دوباره بسته شود.»

```tsx
function Accordion({ items }: { items: { q: string; a: string }[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);  // فقط index!

  return items.map((item, i) => (
    <div key={i}>
      <button
        onClick={() => setOpenIndex(openIndex === i ? null : i)}
        aria-expanded={openIndex === i}       // a11y امتیاز می‌آورد!
      >
        {item.q}
      </button>
      {openIndex === i && <p>{item.a}</p>}
    </div>
  ));
}
```

**بگو:** به‌جای آرایه open ها، یک index — چون «یکی باز» یعنی state تک‌مقداری است. `aria-expanded` برای دسترس‌پذیری. و نسخه چند‌بازشو: `Set<number>`.

---

## تمرین ۵ — Timer (شمارش معکوس)

**صورت مساله:** «تایمر ۱۰ ثانیه‌ای که به صفر که رسید متوقف شود.»

```tsx
function Countdown({ from = 10 }: { from?: number }) {
  const [left, setLeft] = useState(from);

  useEffect(() => {
    if (left === 0) return;
    const id = setInterval(() => setLeft((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(id);       // در هر تغییر و unmount پاک شود
  }, [left !== 0]);                        // ترفند: با رسیدن به صفر، interval نمی‌سازد

  return <span>{left}</span>;
}
```

**بگو:** cleanup حیاتی است (گر نشود interval های همزمان انباشته می‌شوند). فرم تابعی چون وابسته به مقدار قبلی است. نسخه حرفه‌ای‌تر: `setInterval` یک‌بار + چک داخلش.

---

## تمرین ۶ — Infinite Scroll

**صورت مساله:** «لیست پست‌ها که با اسکرول به انتها صفحه بعدی لود شود.»

```tsx
function Feed() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);

  const sentinelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = sentinelRef.current;
    if (!node || !hasMore) return;
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) loadMore();
    });
    obs.observe(node);
    return () => obs.disconnect();
  }, [hasMore, cursor]);

  async function loadMore() {
    const res = await fetch(`/api/posts?cursor=${cursor ?? ""}`);
    const { items, nextCursor } = await res.json();
    setPosts((p) => [...p, ...items]);       // فرم تابعی — با داده جدید ادغام
    setCursor(nextCursor ?? null);
    setHasMore(Boolean(nextCursor));
  }

  return (
    <>
      {posts.map((p) => <Card key={p.id} post={p} />)}
      {hasMore && <div ref={sentinelRef} />}
    </>
  );
}
```

**بگو:** cursor pagination (نه page number — چون insert جدید باعث تکرار می‌شود) + IntersectionObserver (بهتر از scroll listener که هر اسکرول فایر می‌شود).

---

## تمرین ۷ — Form با اعتبارسنجی زنده

**صورت مساله:** «فرم ثبت‌نام: ایمیل معتبر، پسورد ۸+ کاراکتر، نمایش خطا زیر فیلد، دکمه disable تا معتبر.»

```tsx
function Signup() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [touched, setTouched] = useState({ email: false, password: false });

  const errors = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? null : "ایمیل نامعتبر",
    password: form.password.length >= 8 ? null : "حداقل ۸ کاراکتر",
  };
  const isValid = !errors.email && !errors.password;

  return (
    <form onSubmit={(e) => { e.preventDefault(); isValid && submit(form); }}>
      <input value={form.email}
             onChange={(e) => setForm({ ...form, email: e.target.value })}
             onBlur={() => setTouched((t) => ({ ...t, email: true }))} />
      {touched.email && errors.email && <p className="err">{errors.email}</p>}
      {/* پسورد مشابه */}
      <button disabled={!isValid}>ثبت‌نام</button>
    </form>
  );
}
```

**بگو:** validation = محاسبه مشتق‌شده در رندر (نه state جدا — single source of truth!)؛ `touched` تا خطا از اول تایپ نمایش داده نشود؛ واقعی‌ترش: zod + سرور.

---

## تمرین ۸ — Grid فیلترشده (ترکیبی — چاشنی نهایی)

**صورت مساله:** «لیست محصولات با سرچ و فیلتر دسته، همگام با URL.»

```tsx
import { useSearchParams, useRouter, usePathname } from "next/navigation";

function Products({ products }: { products: Product[] }) {   // داده از Server Component
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const q = params.get("q") ?? "";
  const cat = params.get("cat") ?? "all";

  function update(key: string, value: string) {
    const next = new URLSearchParams(params);
    value ? next.set(key, value) : next.delete(key);
    router.push(`${pathname}?${next}`);
  }

  const visible = products.filter((p) =>
    p.title.includes(q) && (cat === "all" || p.category === cat)
  );

  return (
    <>
      <input defaultValue={q}
             onChange={(e) => update("q", e.target.value)} />
      {/* ... فیلتر دسته ... */}
      {visible.map((p) => <Card key={p.id} product={p} />)}
    </>
  );
}
```

**بگو:** فیلتر در URL → shareable، back-safe، رندر سروری دوباره؛ `defaultValue` (uncontrolled) تا URL منبع حقیقت باشد و state تکراری نسازم؛ در پروژه واقعی debounce هم می‌گذارم (تمرین ۱!) — اتصال دو تمرین = امتیاز بزرگ.

---

## ✅ جمع‌بندی فصل

- هشت تمرین پوشش می‌دهند: hook سفارشی، fetch/حالت‌ها، CRUD، state تک‌مقداری، interval/_cleanup_، IntersectionObserver، فرم مشتق‌شده، URL-as-state
- همیشه: سوال شفاف‌سازی → بلند فکر → ساده شروع → edge case → تست با مثال
- امتیازهای مکمل: a11y، empty state، immutable update، فرم تابعی setState

## 📝 تمرین فصل ۸

1. هشت تمرین را با تایمر ۲۰ دقیقه‌ای حل کن (هر روز دو تا، هفته‌ای ۴ روز) — **بلند حرف بزن**.
2. تمرین ۲ را با AbortController بهتر کن (لغو fetch واقعی، نه فقط ignore).
3. تمرین ۶ را با لغو درخواست قبلی کامل کن (کاربر اسکرولش سریع است!).
4. چالش ترکیبی: debounce (۱) + infinite scroll (۶) در یک کامپوننت جستجوی زنده.
5. یک تمرین از مصاحبه واقعی (آنلاین سرچ کن "frontend live coding interview task") پیدا و حل کن و به این لیست اضافه کن.

<details><summary>چک‌لیست روز مصاحبه لایو-کدینگ</summary>

- [ ] ادیتور را قبل شروع کنfigur کن (فونت بزرگ‌تر، افزونه‌ها)
- [ ] سوال را بازگو کن + یک سوال شفاف‌سازی
- [ ] ساختار را بلند بگو قبل از تایپ
- [ ] اسم متغیرهای معنادار — حتی در کد سریع
- [ ] edge case را خودت بگو قبل اینکه بپرسند
- [ ] آخرش با یک مثال ذهنی تست کن و بلند بگو
- [ ] اگر گیر کردی: سکوت ممنوع — بلند فکر کن و راه ساده‌تر را پیشنهاد بده
</details>

➡️ **فصل بعد:** System Design برای فرانت‌کار — با پاسخ نمونه کامل.
