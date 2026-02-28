# Plan: Markdown → JSON Build Pipeline + Dynamic Juz Renderer

## Context

The project has 22 bilingual markdown files per juz (in `juz1/en/` and `juz1/ms/`) and a `template/template.html` with the full design system. The goal is to stop manually compiling HTML and instead:

1. Parse markdown into structured JSON at build time
2. Have a single dynamic `juz-page.html` that fetches the JSON and renders the page — with both en/ms language switching and dark/light theme, all statically

**Recommendation: YES — convert to JSON first.** Reasons:

- Markdown parsing in the browser requires an external library; JSON needs none
- JSON gives typed, structured data the renderer can loop over cleanly
- Language switching is instant (no re-fetch; JSON already holds both `en` and `ms` objects)
- Build step is a single `python3 build/build.py --juz 1` command, no npm needed

---

## Folder Structure (After Implementation)

```
quranicstudies/
├── data/
│   └── juz1.json               ← build output, one per juz
├── build/
│   └── build.py                ← Python 3 stdlib only
├── juz-page.html               ← single universal renderer
├── juz1/
│   ├── en/  (22 .md files)
│   └── ms/  (22 .md files)
├── template/
│   └── template.html           ← CSS/design reference (unchanged)
├── index.html                  ← update href to juz-page.html?juz=N
└── serve.sh                    ← python3 -m http.server 8080
```

---

## Step 1 — JSON Schema

Each `juzN.json` has this shape:

```json
{
  "juz": 1,
  "meta": {
    "title": { "en": "Juz 1 — The Opening", "ms": "Juz 1 — Pembuka" },
    "arabic_name": "الجزء الأول",
    "night": 1,
    "reader": "A",
    "quote": { "en": "...", "ms": "...", "ref": "17:9" }
  },
  "toc": [
    { "id": "section-01", "en": "Surah Al-Fatiha — Introduction", "ms": "Surah Al-Fatiha — Pengenalan" }
  ],
  "sections": [
    {
      "id": "section-01",
      "type": "surah-intro",
      "surah_number": 1,
      "en": {
        "arabic_name": "...", "name": "...", "classification": "Makkan",
        "verses": 7, "epithet": "...", "background": "...", "desc": "..."
      },
      "ms": { }
    },
    {
      "id": "section-02",
      "type": "passage",
      "surah_number": 1,
      "verse_start": 1,
      "verse_end": 3,
      "en": {
        "title": "Basmalah, Praise & The Names of Allah",
        "theme": "...",
        "arabic": "بِسْمِ اللَّهِ...",
        "translation": "In the name of Allah...",
        "explanation": ["paragraph 1", "paragraph 2"],
        "scholars": [
          { "name": "Tafsir Ibn Kathir", "text": "..." },
          { "name": "Tafsir Al-Jalalayn", "text": "..." },
          { "name": "Tafsir As-Sa'di", "text": "..." }
        ],
        "lessons": ["🌿 Lesson 1", "🌊 Lesson 2"]
      },
      "ms": { }
    },
    {
      "id": "section-21",
      "type": "themes-summary",
      "en": {
        "title": "Overarching Themes of Juz 1",
        "opening_quote": { "text": "...", "ref": "2:2" },
        "themes": [
          { "icon": "🕌", "title": "Tawhīd — Pure Monotheism", "body": "...", "table": null }
        ],
        "summary_table": [{ "principle": "Worship Allah alone", "verse": "1:5" }],
        "closing_reflection": { "text": "...", "ref": "2:127–128" }
      },
      "ms": { }
    }
  ]
}
```

**Key design choices:**

- `arabic` field is always under `en` (Arabic text doesn't change by language)
- `sections` is a flat ordered array — renderer loops and switches on `type`
- `explanation` is a `string[]` (one entry per paragraph), not raw HTML

---

## Step 2 — `build/build.py`

### Invocation

```bash
python3 build/build.py --juz 1      # single juz
python3 build/build.py --all        # all juzN/ folders with en/ + ms/
```

### File type detection by filename

```python
def detect_type(filename):
    if re.search(r'-introduction\.md$', filename): return 'surah-intro'
    if re.search(r'themes', filename, re.I):        return 'themes-summary'
    return 'passage'
```

### Core parsing approach

Split file into named sections by `## Heading`:

```python
def split_sections(text):
    sections = {}; current_key = '__preamble__'; buf = []
    for line in text.splitlines():
        if line.startswith('## '):
            sections[current_key] = '\n'.join(buf)
            current_key = line[3:].strip(); buf = []
        else:
            buf.append(line)
    sections[current_key] = '\n'.join(buf)
    return sections
```

This yields keys like `Arabic Text`, `Translation`, `Explanation`, `Scholar Callouts`, `✨ Key Lessons`. Both en/ms use the same `##` heading hierarchy; only the words differ — parser uses key matching by presence, not exact string.

### Key parsing rules per file type

| Section | Rule |
|---|---|
| Arabic text | Extract `>` blockquote lines, strip leading `>` |
| Translation | Same blockquote extraction, strip surrounding `*...*` |
| Explanation | Split on blank lines → list of paragraphs |
| Scholar callouts | Split `## Scholar Callouts` body on `###` → list of `{name, text}` |
| Key Lessons | Filter lines starting with `- ` → strip `- ` prefix → list |
| Themes `###` | Split themes section on `### N.` → `{icon, title, body, table}` |
| Markdown tables | Lines starting with `|` → parsed into array of objects |

### En/Ms pairing

Files are sorted alphabetically; `en/02-fatiha-1-3.md` is always paired with `ms/02-fatiha-1-3.md`. Both produce the same section object; parser builds `en` and `ms` sub-objects from each respective file.

### Output

`data/juz1.json` written with `json.dumps(data, ensure_ascii=False, indent=2)`.

---

## Step 3 — `juz-page.html`

Based on `template/template.html` (all CSS verbatim). Replace static HTML content with a JS renderer. Add a second fixed button for language.

### Boot sequence

```javascript
const juzNum = new URLSearchParams(location.search).get('juz') || '1';
fetch(`data/juz${juzNum}.json`)
  .then(r => r.json())
  .then(data => {
    renderPage(data, localStorage.getItem('tafsir-lang') || 'en');
    initThemeToggle();
    initLangToggle(data);
    initTocHighlight();
  });
```

### Language toggle button

Added alongside existing theme toggle:

```html
<button id="lang-toggle" title="Switch language">EN</button>
```

Positioned with CSS at `right: 4.5rem` (left of the theme button). On click, toggles `tafsir-lang` in localStorage between `en` and `ms`, then calls `renderPage(data, newLang)` — full re-render of `<main>`, hero, and TOC. No page reload. No network request (data is already in memory).

### Section renderer switch

```javascript
function renderSections(data, lang) {
  const main = document.getElementById('main-content');
  main.innerHTML = '';
  data.sections.forEach(section => {
    if      (section.type === 'surah-intro')   main.appendChild(buildSurahBanner(section, lang));
    else if (section.type === 'passage')        main.appendChild(buildPassage(section, lang));
    else if (section.type === 'themes-summary') main.appendChild(buildThemesSummary(section, lang));
  });
}
```

### Static UI label strings

Not from JSON, hardcoded in JS:

```javascript
const UI = {
  en: { toc: '📖 Contents', translation: 'Translation', lessons: '✨ Key Lessons' },
  ms: { toc: '📖 Kandungan', translation: 'Terjemahan',  lessons: '✨ Pengajaran Utama' }
};
```

---

## Step 4 — `serve.sh`

```bash
#!/bin/bash
python3 -m http.server 8080
```

`fetch()` is blocked on `file://` in Chrome/Firefox. This one-line script (already available on every Mac) is the only "tool" needed to develop locally. Deployment on GitHub Pages / Netlify / Vercel works natively.

---

## Step 5 — `index.html` Minor Update

- Update juz card `href` from `juz1.html` → `juz-page.html?juz=1` (as each juz is migrated)
- Standardise localStorage key from `juz23-theme` → `tafsir-theme` across all pages

---

## Critical Files

| File | Role |
|---|---|
| `template/template.html` | CSS source — copy verbatim into `juz-page.html` |
| `juz1/en/02-fatiha-1-3.md` | Canonical passage format for `build.py` parsing tests |
| `juz1/en/05-baqarah-introduction.md` | Richest surah-intro (has table, hadith, subsections list) |
| `juz1/en/21-themes-summary.md` | Most complex file type (nested `###`, tables, closing quote) |
| `juz1.html` | Reference for the hero, info cards, and TOC HTML patterns |

---

## Verification

1. `python3 build/build.py --juz 1` → inspect `data/juz1.json`; verify all 21 sections present with correct types, Arabic text intact, both `en` and `ms` keys populated
2. `python3 -m http.server 8080` then open `http://localhost:8080/juz-page.html?juz=1`
3. Verify: all passage cards render, Arabic text displays RTL, dark/light toggle works, en↔ms language toggle re-renders all content without page reload
4. Compare output visually against `juz1.html` to confirm identical styling
