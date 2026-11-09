# -*- coding: utf-8 -*-
"""Build a single RTL Persian PDF-ready HTML from the interview-prep course."""
import re, pathlib, markdown
from pygments.formatters import HtmlFormatter

BASE = pathlib.Path(__file__).resolve().parent.parent
BUILD = BASE / "build"

CHAPTERS = [
    ("README.md", "شروع دوره"),
    ("01-fear-mindset.md", "فصل ۱ — روانشناسی ترس مصاحبه"),
    ("02-cv-portfolio.md", "فصل ۲ — رزومه و پورتفولیو"),
    ("03-finding-applying.md", "فصل ۳ — جستجو و اپلای"),
    ("04-process-stages.md", "فصل ۴ — مراحل مصاحبه"),
    ("05-js-ts-questions.md", "فصل ۵ — ۱۸ سوال JS/TS"),
    ("06-react-questions.md", "فصل ۶ — ۲۰ سوال React"),
    ("07-nextjs-questions.md", "فصل ۷ — ۱۶ سوال Next.js"),
    ("08-live-coding.md", "فصل ۸ — ۸ تمرین Live Coding"),
    ("09-system-design-frontend.md", "فصل ۹ — System Design"),
    ("10-behavioral.md", "فصل ۱۰ — مصاحبه رفتاری (STAR)"),
    ("11-your-questions-salary.md", "فصل ۱۱ — سوالات تو و حقوق"),
    ("12-after-interview.md", "فصل ۱۲ — بعد از مصاحبه"),
    ("13-cheatsheet.md", "فصل ۱۳ — چیت‌شیت و گلاساری"),
    ("14-html-css-questions.md", "فصل ۱۴ — ۲۰ سوال HTML/CSS"),
    ("15-browser-dom-questions.md", "فصل ۱۵ — مرورگر، DOM و تله‌های JS"),
]

ANCHOR = {fn: f"ch{i:02d}" for i, (fn, _) in enumerate(CHAPTERS)}
LINK_RE = re.compile(r"\]\((\.?/?)([\w\-]+\.md)([#\w\-]*)\)")

MD_EXT = ["tables", "fenced_code", "codehilite", "md_in_html", "attr_list", "sane_lists"]
MD_CFG = {"codehilite": {"guess_lang": False}}


def preprocess(text: str) -> str:
    def repl(m):
        target, frag = m.group(2), m.group(3) or ""
        if target in ANCHOR:
            return f"](#{ANCHOR[target]}{frag})"
        return m.group(0)
    text = LINK_RE.sub(repl, text)
    text = re.sub(r"```mermaid\n(.*?)```", lambda m: f'<div class="mermaid">\n{m.group(1)}</div>', text, flags=re.S)
    text = text.replace("<details>", '<details markdown="1" open>')
    text = text.replace("<summary>", '<summary markdown="span">')
    return text


def render_chapter(fn: str, idx: int) -> str:
    raw = (BASE / fn).read_text(encoding="utf-8")
    body = markdown.markdown(preprocess(raw), extensions=MD_EXT, extension_configs=MD_CFG)
    return f'<section class="chapter" id="ch{idx:02d}">{body}</section>'


CSS = """
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Medium.ttf') format('truetype'); font-weight:500; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Bold.ttf') format('truetype'); font-weight:700; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Bold.ttf') format('truetype'); font-weight:700; }

@page { size: A4; margin: 16mm 13mm 18mm 13mm; }

:root {
  --ink:#2a1218; --muted:#83606a; --line:#f2dfe4;
  --primary:#9f1239; --primary-soft:#fff1f2;
  --accent:#c2410c; --accent-soft:#fff7ed;
  --green:#059669; --green-soft:#ecfdf5;
  --amber:#b45309; --amber-soft:#fffbeb;
  --rose:#be123c; --rose-soft:#fff1f2;
  --code-bg:#2b0a17; --code-ink:#f5e8ec;
}
* { box-sizing:border-box; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body {
  direction:rtl; text-align:right;
  font-family:'Vazirmatn', Tahoma, sans-serif;
  color:var(--ink); font-size:11.2pt; line-height:2;
  margin:0; padding:0;
}

/* cover */
.cover {
  page-break-after:always; height:250mm;
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; color:#fff; border-radius:14px; padding:20mm;
  background:linear-gradient(135deg,#4c0519 0%,#9f1239 50%,#e11d48 130%);
}
.cover .badge { background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.35);
  padding:4px 18px; border-radius:999px; font-size:10pt; letter-spacing:.3px; }
.cover h1 { font-size:28pt; line-height:1.7; margin:14px 0 6px; border:none; color:#fff; background:none; }
.cover h2 { font-size:14pt; font-weight:500; color:#ffe4e6; border:none; margin:0; }
.cover .stack { display:flex; gap:10px; margin-top:26px; flex-wrap:wrap; justify-content:center; }
.cover .stack span { background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.3);
  border-radius:10px; padding:6px 16px; font-size:10.5pt; }
.cover .foot { margin-top:40px; font-size:9.5pt; opacity:.85; }

/* toc */
.toc { page-break-after:always; }
.toc h1 { border:none; }
.toc ol { list-style:none; padding:0; counter-reset:toc; }
.toc li { counter-increment:toc; border-bottom:1px dashed var(--line);
  padding:9px 2px; display:flex; justify-content:space-between; align-items:baseline; }
.toc a { text-decoration:none; color:var(--ink); font-weight:500; }
.toc li::before { content:counter(toc); background:var(--primary-soft); color:var(--primary);
  font-weight:700; border-radius:8px; width:30px; height:30px; display:inline-flex;
  align-items:center; justify-content:center; margin-left:14px; flex:none; }
.toc li .desc { color:var(--muted); font-size:9.5pt; }

/* chapters / headings */
.chapter { page-break-before:always; }
h1 {
  font-size:19pt; color:#fff; background:linear-gradient(90deg,#881337,#be123c);
  padding:14px 22px; border-radius:12px; line-height:1.7;
  margin:0 0 18px; page-break-after:avoid;
}
h2 {
  color:var(--primary); font-size:14.5pt; margin:26px 0 10px;
  padding-right:12px; border-right:4px solid var(--primary); line-height:1.8;
  page-break-after:avoid;
}
h3 { color:var(--accent); font-size:12.5pt; margin:20px 0 8px; page-break-after:avoid; }
p { margin:8px 0; }
strong { color:#4c0519; }
a { color:var(--primary); text-decoration:none; }

/* lists */
ul, ol { padding-right:1.6em; padding-left:0; margin:8px 0; }
li { margin:3px 0; }
li::marker { color:var(--primary); font-weight:700; }
input[type="checkbox"] { accent-color:var(--primary); }

/* tables */
table { border-collapse:collapse; width:100%; margin:12px 0; font-size:10pt;
  border-radius:10px; overflow:hidden; page-break-inside:avoid; }
.table-break table { page-break-inside:auto; border-radius:0; }
.table-break thead { display:table-header-group; }
.table-break tr { page-break-inside:avoid; }
th { background:linear-gradient(90deg,#881337,#be123c); color:#fff; font-weight:700; }
th, td { border:1px solid #efd6dc; padding:6px 10px; text-align:right; vertical-align:top; }
tbody tr:nth-child(even) { background:#fdf6f7; }

/* code */
pre, code, kbd { font-family:'JetBrains Mono','Vazirmatn',Consolas,monospace; direction:ltr; }
code { background:#fff1f2; color:#9f1239; padding:1px 6px; border-radius:5px;
  font-size:8.8pt; unicode-bidi:embed; }
pre { background:var(--code-bg); color:var(--code-ink); direction:ltr; text-align:left;
  padding:13px 16px; border-radius:12px; overflow-x:hidden; font-size:8.6pt;
  line-height:1.65; margin:10px 0; border:1px solid #4c0519; page-break-inside:avoid; }
pre code { background:none; color:inherit; padding:0; font-size:inherit; }
.codehilite { background:var(--code-bg); border-radius:12px; margin:10px 0; page-break-inside:avoid; }
.codehilite pre { margin:0; border:none; }
.codehilite .k,.codehilite .kd,.codehilite .kn,.codehilite .ow { color:#fda4af; }
.codehilite .s,.codehilite .s1,.codehilite .s2,.codehilite .sd { color:#86efac; }
.codehilite .n,.codehilite .na,.codehilite .nx { color:#f5e8ec; }
.codehilite .nf { color:#fde047; }
.codehilite .mi,.codehilite .mf { color:#fbcfe8; }
.codehilite .o,.codehilite .p { color:#d8a4b0; }
.codehilite .nb,.codehilite .nv { color:#7dd3fc; }
.codehilite .err { color:#f5e8ec; background:none; border:none; }
.codehilite .c,.codehilite .c1,.codehilite .cm,.codehilite .cp { color:#c88296 !important; font-style:italic; }
.codehilite .nt { color:#f0abfc; }
.codehilite .nd { color:#fde047; }

/* blockquotes */
blockquote {
  margin:12px 0; padding:10px 16px; border-radius:12px;
  border-right:5px solid var(--primary); background:var(--primary-soft);
  page-break-inside:avoid;
}
blockquote p { margin:4px 0; }
blockquote p:first-child { font-weight:500; }
blockquote:has(> p:first-child strong:contains("⚠")) { background:var(--amber-soft); border-right-color:var(--amber); }
blockquote:has(> p:first-child strong:contains("🚨")) { background:var(--rose-soft); border-right-color:var(--rose); }
blockquote:has(> p:first-child strong:contains("💡")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🔑")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🎯")) { background:var(--primary-soft); border-right-color:var(--primary); }
blockquote:has(> p:first-child strong:contains("🚩")) { background:var(--rose-soft); border-right-color:var(--rose); }
blockquote:has(> p:first-child strong:contains("💪")) { background:var(--primary-soft); border-right-color:var(--primary); }

/* hr, details */
hr { border:none; border-top:2px dashed var(--line); margin:22px 0; }
details { background:#fdf6f7; border:1px solid var(--line); border-radius:10px;
  padding:8px 14px; margin:10px 0; page-break-inside:avoid; }
summary { cursor:pointer; font-weight:700; color:var(--green); }

/* mermaid */
.mermaid {
  background:#fff; border:1px solid var(--line); border-radius:12px;
  padding:10px; margin:12px 0; text-align:center; page-break-inside:avoid;
  display:flex; justify-content:center;
}
.mermaid svg { max-width:100%; height:auto; }

del { color:var(--muted); }
em { color:#4c0519; }
"""

PYGMENTS_CSS = HtmlFormatter(style="default").get_style_defs(".codehilite")

COVER = """
<section class="cover">
  <div class="badge">آموزش صفر تا صد — همراه با جواب‌های کامل</div>
  <h1>مصاحبه شغلی فرانت‌اند<br/>از ترس تا تسلط</h1>
  <h2>React و Next.js — ۸۹ سوال با جواب، ۸ تمرین لایو‌کدینگ و برنامه شکستن ترس</h2>
  <div class="stack">
    <span>شکستن ترس</span><span>رزومه و پورتفولیو</span><span>۸۹ سوال با جواب</span>
    <span>Live Coding</span><span>System Design</span><span>مذاکره حقوق</span>
  </div>
  <div class="foot">۱۵ فصل · جواب نمونه STAR · چک‌لیست روز مصاحبه · برنامه ۹۰ روز اول</div>
</section>
"""

DESCS = {
    "README.md": "فلسفه دوره و برنامه ۳ هفته",
    "01-fear-mindset.md": "۳ ریشه ترس، reframe، thinking out loud",
    "02-cv-portfolio.md": "رزومه عددی، ۳ پروژه پرچمدار، LinkedIn",
    "03-finding-applying.md": "قیف اپلای، DM، جدول پیگیری",
    "04-process-stages.md": "screening تا offer، جدول آمادگی",
    "05-js-ts-questions.md": "event loop، closure، debounce",
    "06-react-questions.md": "VDOM، keys، memo، React 19",
    "07-nextjs-questions.md": "SSG/ISR، RSC، Server Action",
    "08-live-coding.md": "۸ تمرین با کد کامل و پروتکل رفتار",
    "09-system-design-frontend.md": "قالب ۵ مرحله + ۲ پاسخ نمونه",
    "10-behavioral.md": "STAR + ۴ جواب نمونه کامل",
    "11-your-questions-salary.md": "سوالات تو، red flags، مذاکره",
    "12-after-interview.md": "follow-up، رد شدن، ۹۰ روز اول",
    "13-cheatsheet.md": "چک‌لیست‌ها + گلاساری + نقشه راه",
    "14-html-css-questions.md": "HTML/CSS از هندبوک فرانت — بدون تکرار",
    "15-browser-dom-questions.md": "DOM/مرورگر + خروجی‌بگوهای کوییز JS",
}


def build_toc() -> str:
    items = []
    for i, (fn, title) in enumerate(CHAPTERS):
        items.append(f'<li><a href="#ch{i:02d}">{title}</a><span class="desc">{DESCS.get(fn, "")}</span></li>')
    return f'<section class="toc"><h1>فهرست مطالب</h1><ol>{"".join(items)}</ol></section>'


def main():
    parts = [COVER, build_toc()]
    for i, (fn, _) in enumerate(CHAPTERS):
        parts.append(render_chapter(fn, i))
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"/>
<title>دوره مصاحبه شغلی فرانت‌اند</title>
<style>{CSS}
{PYGMENTS_CSS}
</style></head>
<body>{''.join(parts)}
<script src="mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad:true, theme:'base',
  themeVariables: {{ fontFamily:'Vazirmatn, Tahoma', fontSize:'13px',
    primaryColor:'#fff1f2', primaryBorderColor:'#9f1239', primaryTextColor:'#2a1218',
    lineColor:'#64748b', secondaryColor:'#fff7ed', tertiaryColor:'#fdf6f7' }},
  flowchart: {{ htmlLabels:true, curve:'basis' }} }});</script>
</body></html>"""
    out = BUILD / "course.html"
    out.write_text(html, encoding="utf-8")
    print(f"OK -> {out}  ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
