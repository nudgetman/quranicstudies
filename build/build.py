#!/usr/bin/env python3
"""
build.py — Markdown → JSON pipeline for the Qur'anic Tafsir Series.

Usage:
  python3 build/build.py --juz 1      # single juz
  python3 build/build.py --all        # all juzN/ folders with en/ + ms/
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


# ─── File type detection ──────────────────────────────────────────────────────

def detect_type(filename):
    if re.search(r'-introduction\.md$', filename):
        return 'surah-intro'
    if re.search(r'themes', filename, re.I):
        return 'themes-summary'
    return 'passage'


# ─── Core markdown utilities ──────────────────────────────────────────────────

def split_sections(text):
    """Split markdown into named sections by ## headings.
    Returns dict: heading_text → section_body_text.
    The key '__preamble__' holds everything before the first ## heading.
    """
    sections = {}
    current_key = '__preamble__'
    buf = []
    for line in text.splitlines():
        if line.startswith('## '):
            sections[current_key] = '\n'.join(buf)
            current_key = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    sections[current_key] = '\n'.join(buf)
    return sections


def extract_blockquote(text):
    """Extract content from > blockquote lines, joined into one string."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('> '):
            lines.append(stripped[2:].strip())
    return ' '.join(lines)


def strip_italic(text):
    """Strip surrounding *text* markers (not **bold**)."""
    text = text.strip()
    if text.startswith('*') and text.endswith('*') and not text.startswith('**'):
        text = text[1:-1]
    return text


def clean_markdown_inline(text):
    """Remove inline markdown formatting: **bold**, *italic*, `code`."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text.strip()


def extract_meta_field(preamble, *field_names):
    """Extract **Field:** value from preamble, trying multiple field names.
    Returns the cleaned string value or '' if not found.
    """
    for field in field_names:
        pattern = rf'\*\*{re.escape(field)}:\*\*\s*(.+?)(?:\s*\\?\s*$|\n)'
        m = re.search(pattern, preamble, re.MULTILINE)
        if m:
            val = m.group(1).strip()
            val = clean_markdown_inline(val)
            return val
    return ''


def parse_paragraphs(text):
    """Split text on blank lines → list of non-empty paragraph strings."""
    paras = []
    buf = []
    for line in text.splitlines():
        if not line.strip():
            if buf:
                paras.append(' '.join(buf).strip())
                buf = []
        else:
            # Skip pure markdown separators
            if re.match(r'^---+$', line.strip()):
                if buf:
                    paras.append(' '.join(buf).strip())
                    buf = []
                continue
            buf.append(line.strip())
    if buf:
        paras.append(' '.join(buf).strip())
    return [p for p in paras if p]


def parse_scholars(text):
    """Parse ### Scholar Name sub-sections into list of {name, text}."""
    scholars = []
    # Split on ### headings
    parts = re.split(r'^### ', text, flags=re.MULTILINE)
    for part in parts:
        if not part.strip():
            continue
        lines = part.strip().splitlines()
        if not lines:
            continue
        # First line is the scholar name (may have emoji prefix like 📖)
        raw_name = lines[0].strip()
        # Remove leading emoji/non-word characters
        name_match = re.search(r'[A-Za-z\u0600-\u06FF]', raw_name)
        name = raw_name[name_match.start():].strip() if name_match else raw_name

        # Collect body text (including blockquote lines)
        body_parts = []
        for line in lines[1:]:
            s = line.strip()
            if not s or re.match(r'^---+$', s):
                continue
            if s.startswith('> '):
                body_parts.append(s[2:].strip())
            else:
                body_parts.append(s)

        body = ' '.join(body_parts)
        body = clean_markdown_inline(body)
        scholars.append({'name': name, 'text': body})

    return scholars


def parse_lessons(text):
    """Parse - bullet lines into list of strings."""
    lessons = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('- '):
            lessons.append(s[2:].strip())
    return lessons


# ─── Passage file parser ──────────────────────────────────────────────────────

def parse_passage_file(text, lang='en'):
    """Parse a passage markdown file.

    Returns:
        (data_dict, surah_num, verse_start, verse_end)
    Where data_dict has all fields needed for section['en'] or section['ms'].
    For lang='en', data_dict also includes 'arabic'.
    """
    secs = split_sections(text)
    preamble = secs.get('__preamble__', '')

    # ── Title from # heading ──
    title_match = re.search(r'^# (.+)$', preamble, re.MULTILINE)
    full_title = title_match.group(1).strip() if title_match else ''
    # Section title is the part after the · separator
    if '·' in full_title:
        title = full_title.split('·', 1)[1].strip()
    else:
        title = full_title

    # ── Theme ──
    theme = extract_meta_field(preamble, 'Theme', 'Tema')

    # ── Surah number from **Surah:** Al-Fatiha (1) · ... ──
    surah_field = extract_meta_field(preamble, 'Surah')
    surah_num = 1
    surah_match = re.search(r'\((\d+)\)', surah_field)
    if surah_match:
        surah_num = int(surah_match.group(1))

    # ── Verse range from **Verses:** / **Ayat:** 1–3 ──
    verse_field = extract_meta_field(preamble, 'Verses', 'Ayat')
    verse_start = None
    verse_end = None
    range_match = re.search(r'(\d+)\s*[–—-]\s*(\d+)', verse_field)
    if range_match:
        verse_start = int(range_match.group(1))
        verse_end = int(range_match.group(2))
    else:
        single_match = re.search(r'(\d+)', verse_field)
        if single_match:
            verse_start = verse_end = int(single_match.group(1))

    # ── Arabic text (extract regardless of lang; only stored under en) ──
    arabic_text = ''
    for key in secs:
        if re.search(r'arabic|teks arab', key, re.I):
            arabic_text = extract_blockquote(secs[key]).strip()
            break

    # ── Translation ──
    translation = ''
    for key in secs:
        if re.match(r'^(translation|terjemahan)$', key, re.I):
            raw = extract_blockquote(secs[key])
            translation = strip_italic(raw)
            break

    # ── Explanation ──
    explanation = []
    for key in secs:
        if re.match(r'^(explanation|penjelasan)$', key, re.I):
            explanation = parse_paragraphs(secs[key])
            break

    # ── Scholar callouts ──
    scholars = []
    for key in secs:
        if re.search(r'scholar|callout|petikan ulama', key, re.I):
            scholars = parse_scholars(secs[key])
            break

    # ── Key lessons ──
    lessons = []
    for key in secs:
        if re.search(r'lesson|pengajaran', key, re.I):
            lessons = parse_lessons(secs[key])
            break

    data = {
        'title': title,
        'theme': theme,
        'translation': translation,
        'explanation': explanation,
        'scholars': scholars,
        'lessons': lessons,
    }
    if lang == 'en':
        data['arabic'] = arabic_text

    return data, surah_num, verse_start, verse_end


# ─── Surah intro file parser ──────────────────────────────────────────────────

def parse_surah_intro_file(text, lang='en'):
    """Parse a surah introduction file.

    Returns dict with keys:
        surah_number, arabic_name, name, classification, verses,
        epithet, background, desc
    """
    secs = split_sections(text)
    preamble = secs.get('__preamble__', '')

    # ── Surah number ──
    surah_num_str = extract_meta_field(preamble, 'Surah')
    try:
        surah_num = int(surah_num_str)
    except (ValueError, TypeError):
        surah_num = 1

    # ── Arabic name ──
    arabic_name = extract_meta_field(preamble, 'Arabic Name', 'Nama Arab')

    # ── English / Malay display name ──
    name = extract_meta_field(
        preamble, 'English Name', 'Nama Melayu', 'Nama English', 'Malay Name'
    )
    if not name:
        title_match = re.search(r'^# (.+)$', preamble, re.MULTILINE)
        name = title_match.group(1).strip() if title_match else ''

    # ── Classification ──
    classification = extract_meta_field(preamble, 'Classification', 'Klasifikasi')

    # ── Verses ──
    verses_str = extract_meta_field(preamble, 'Verses', 'Bilangan Ayat')
    try:
        verses = int(verses_str)
    except (ValueError, TypeError):
        verses = 0

    # ── Epithet / Distinction ──
    epithet = extract_meta_field(preamble, 'Epithet', 'Gelaran', 'Distinction')

    # ── Background section ──
    background = ''
    for key in secs:
        if re.match(r'^(background|latar belakang)$', key, re.I):
            background = secs[key].strip()
            break

    # desc = first paragraph of background
    desc_paras = parse_paragraphs(background)
    desc = desc_paras[0] if desc_paras else ''

    return {
        'surah_number': surah_num,
        'arabic_name': arabic_name,
        'name': name,
        'classification': classification,
        'verses': verses,
        'epithet': epithet,
        'background': background,
        'desc': desc,
    }


# ─── Themes summary file parser ───────────────────────────────────────────────

def parse_themes_file(text, lang='en'):
    """Parse the themes summary file.

    Returns dict with keys:
        title, opening_quote, themes, summary_table, closing_reflection
    """
    secs = split_sections(text)
    preamble = secs.get('__preamble__', '')

    # ── Title from # heading ──
    title_match = re.search(r'^# (.+)$', preamble, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else 'Overarching Themes'

    # ── Opening quote from preamble > blockquote ──
    opening_quote_text = ''
    opening_quote_ref = ''
    for line in preamble.splitlines():
        s = line.strip()
        if s.startswith('> '):
            raw = s[2:].strip()
            ref_match = re.search(r'—\s*(.+)$', raw)
            if ref_match:
                opening_quote_ref = ref_match.group(1).strip()
                opening_quote_text = strip_italic(raw[:ref_match.start()].strip())
            else:
                opening_quote_text = strip_italic(raw)
            break

    # ── Parse themes from section that contains ### sub-headings ──
    themes = []
    for key, content in secs.items():
        if key == '__preamble__':
            continue
        if '### ' in content:
            # Split on "### N. " or "### " directly
            theme_parts = re.split(r'^### \d+\.\s*', content, flags=re.MULTILINE)
            if len(theme_parts) <= 1:
                # Try splitting without number
                theme_parts = re.split(r'^### ', content, flags=re.MULTILINE)

            for part in theme_parts:
                if not part.strip():
                    continue
                lines = part.strip().splitlines()
                if not lines:
                    continue
                # First line: "🕌 Tawhīd — Pure Monotheism" or similar
                header = lines[0].strip()
                # Extract icon (first non-alphanumeric token) and title
                icon = ''
                theme_title = header
                icon_match = re.match(r'^(\S+)\s+(.+)$', header)
                if icon_match:
                    candidate = icon_match.group(1)
                    # Emoji check: if first char is not ASCII letter/digit, treat as icon
                    if candidate and not candidate[0].isascii() or not candidate[0].isalnum():
                        icon = candidate
                        theme_title = icon_match.group(2)

                # Collect body text (skip table rows and separator lines)
                body_lines = []
                table_rows = []
                in_table = False
                for line in lines[1:]:
                    s = line.strip()
                    if re.match(r'^---+$', s):
                        break  # End of this theme block
                    if s.startswith('|'):
                        # Table row — skip header/separator
                        if re.match(r'^\|[-|:\s]+\|$', s):
                            continue
                        cells = [c.strip() for c in s.strip('|').split('|')]
                        table_rows.append(cells)
                        in_table = True
                    elif s:
                        body_lines.append(s)

                body = clean_markdown_inline(' '.join(body_lines).strip())

                # Build table if present
                table = None
                if table_rows and len(table_rows[0]) >= 2:
                    # Skip header row if it looks like a header
                    data_rows = table_rows
                    table = [{'col1': r[0], 'col2': r[1]} for r in data_rows]

                themes.append({
                    'icon': icon,
                    'title': theme_title,
                    'body': body,
                    'table': table,
                })
            break  # Only process the first themes section

    # ── Summary table ──
    summary_table = []
    for key, content in secs.items():
        if re.search(r'summary table|jadual ringkasan', key, re.I):
            for line in content.splitlines():
                s = line.strip()
                if not s.startswith('|'):
                    continue
                if re.match(r'^\|[-|:\s]+\|$', s):
                    continue
                cells = [c.strip() for c in s.strip('|').split('|')]
                if len(cells) >= 2:
                    # Skip header row
                    if cells[0] in ('Principle', 'Prinsip', 'Verse', 'Ayat'):
                        continue
                    summary_table.append({
                        'principle': cells[0],
                        'verse': cells[1],
                    })
            break

    # ── Closing reflection ──
    closing_text = ''
    closing_ref = ''
    for key, content in secs.items():
        if re.search(r'closing|renungan|reflection', key, re.I):
            for line in content.splitlines():
                s = line.strip()
                if s.startswith('> '):
                    raw = s[2:].strip()
                    ref_match = re.search(r'—\s*(.+)$', raw)
                    if ref_match:
                        closing_ref = ref_match.group(1).strip()
                        closing_text = strip_italic(raw[:ref_match.start()].strip())
                    else:
                        closing_text = strip_italic(raw)
                    break
            break

    return {
        'title': title,
        'opening_quote': {'text': opening_quote_text, 'ref': opening_quote_ref},
        'themes': themes,
        'summary_table': summary_table,
        'closing_reflection': {'text': closing_text, 'ref': closing_ref},
    }


# ─── Overview file parser ─────────────────────────────────────────────────────

def parse_overview(en_text, ms_text):
    """Extract juz-level metadata from 00-overview.md files."""
    def get_quote(text):
        for line in text.splitlines():
            s = line.strip()
            if s.startswith('> '):
                raw = s[2:].strip()
                ref_match = re.search(r'—\s*(.+)$', raw)
                if ref_match:
                    ref = ref_match.group(1).strip()
                    quote_text = strip_italic(raw[:ref_match.start()].strip())
                    return quote_text, ref
        return '', ''

    en_q, ref = get_quote(en_text)
    ms_q, _ = get_quote(ms_text)
    return {'quote': {'en': en_q, 'ms': ms_q, 'ref': ref}}


# ─── Juz builder ─────────────────────────────────────────────────────────────

def build_juz(juz_num):
    """Parse all markdown files for a juz and return the structured data dict."""
    juz_dir = ROOT / f'juz{juz_num}'
    en_dir = juz_dir / 'en'
    ms_dir = juz_dir / 'ms'

    if not en_dir.exists() or not ms_dir.exists():
        print(f'ERROR: juz{juz_num}/en/ or juz{juz_num}/ms/ not found', file=sys.stderr)
        return None

    en_files = sorted(en_dir.glob('*.md'))

    # ── Overview / meta ──
    overview_en_path = en_dir / '00-overview.md'
    overview_ms_path = ms_dir / '00-overview.md'
    overview_en = overview_en_path.read_text(encoding='utf-8') if overview_en_path.exists() else ''
    overview_ms = overview_ms_path.read_text(encoding='utf-8') if overview_ms_path.exists() else ''
    overview_meta = parse_overview(overview_en, overview_ms)

    # ── Derive juz title from first surah-intro file ──
    title_en = f'Juz {juz_num}'
    title_ms = f'Juz {juz_num}'
    for f in en_files:
        if f.name == '00-overview.md':
            continue
        if detect_type(f.name) == 'surah-intro':
            ms_f = ms_dir / f.name
            en_t = f.read_text(encoding='utf-8')
            ms_t = ms_f.read_text(encoding='utf-8') if ms_f.exists() else ''
            secs_en = split_sections(en_t)
            secs_ms = split_sections(ms_t)
            pre_en = secs_en.get('__preamble__', '')
            pre_ms = secs_ms.get('__preamble__', '')
            en_name = extract_meta_field(pre_en, 'English Name', 'Nama Melayu')
            ms_name = extract_meta_field(pre_ms, 'Nama Melayu', 'English Name')
            # Extract subtitle after "—"
            def subtitle(s):
                if '—' in s:
                    return s.split('—', 1)[1].strip()
                return s
            title_en = f'Juz {juz_num} — {subtitle(en_name)}' if en_name else f'Juz {juz_num}'
            title_ms = f'Juz {juz_num} — {subtitle(ms_name)}' if ms_name else f'Juz {juz_num}'
            break

    # Juz-level arabic name lookup (could be extended for all 30 juz)
    arabic_juz_names = {
        1: 'الجزء الأول', 2: 'الجزء الثاني', 3: 'الجزء الثالث',
        4: 'الجزء الرابع', 5: 'الجزء الخامس', 6: 'الجزء السادس',
        7: 'الجزء السابع', 8: 'الجزء الثامن', 9: 'الجزء التاسع',
        10: 'الجزء العاشر', 11: 'الجزء الحادي عشر', 12: 'الجزء الثاني عشر',
        13: 'الجزء الثالث عشر', 14: 'الجزء الرابع عشر', 15: 'الجزء الخامس عشر',
        16: 'الجزء السادس عشر', 17: 'الجزء السابع عشر', 18: 'الجزء الثامن عشر',
        19: 'الجزء التاسع عشر', 20: 'الجزء العشرون', 21: 'الجزء الحادي والعشرون',
        22: 'الجزء الثاني والعشرون', 23: 'الجزء الثالث والعشرون',
        24: 'الجزء الرابع والعشرون', 25: 'الجزء الخامس والعشرون',
        26: 'الجزء السادس والعشرون', 27: 'الجزء السابع والعشرون',
        28: 'الجزء الثامن والعشرون', 29: 'الجزء التاسع والعشرون',
        30: 'الجزء الثلاثون',
    }

    meta = {
        'title': {'en': title_en, 'ms': title_ms},
        'arabic_name': arabic_juz_names.get(juz_num, f'الجزء {juz_num}'),
        'night': juz_num,
        'reader': 'A',
        'quote': overview_meta['quote'],
    }

    sections = []
    toc = []
    section_idx = 0

    for en_file in en_files:
        fname = en_file.name

        # Skip overview file
        if fname == '00-overview.md':
            continue

        ms_file = ms_dir / fname
        if not ms_file.exists():
            print(f'  WARNING: ms/{fname} not found — skipping', file=sys.stderr)
            continue

        en_text = en_file.read_text(encoding='utf-8')
        ms_text = ms_file.read_text(encoding='utf-8')

        ftype = detect_type(fname)
        section_idx += 1
        section_id = f'section-{section_idx:02d}'
        section = {'id': section_id, 'type': ftype}

        if ftype == 'surah-intro':
            en_data = parse_surah_intro_file(en_text, 'en')
            ms_data = parse_surah_intro_file(ms_text, 'ms')

            section['surah_number'] = en_data.pop('surah_number')
            ms_data.pop('surah_number', None)  # not stored under ms

            section['en'] = en_data
            section['ms'] = ms_data

            # TOC label: full # title from each file
            def get_h1(text):
                m = re.search(r'^# (.+)$', text, re.MULTILINE)
                return m.group(1).strip() if m else fname

            toc.append({
                'id': section_id,
                'en': get_h1(en_text),
                'ms': get_h1(ms_text),
            })

        elif ftype == 'passage':
            en_data, surah_num, verse_start, verse_end = parse_passage_file(en_text, 'en')
            ms_data, _, _, _ = parse_passage_file(ms_text, 'ms')

            section['surah_number'] = surah_num
            section['verse_start'] = verse_start
            section['verse_end'] = verse_end
            section['en'] = en_data
            section['ms'] = ms_data

            toc.append({
                'id': section_id,
                'en': en_data['title'],
                'ms': ms_data['title'],
            })

        elif ftype == 'themes-summary':
            en_data = parse_themes_file(en_text, 'en')
            ms_data = parse_themes_file(ms_text, 'ms')

            section['en'] = en_data
            section['ms'] = ms_data

            toc.append({
                'id': section_id,
                'en': en_data['title'],
                'ms': ms_data['title'],
            })

        sections.append(section)

    return {
        'juz': juz_num,
        'meta': meta,
        'toc': toc,
        'sections': sections,
    }


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Build Markdown → JSON for the Qur\'anic Tafsir Series'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--juz', type=int, metavar='N', help='Build juz N')
    group.add_argument('--all', action='store_true', help='Build all juzN/ folders')
    args = parser.parse_args()

    output_dir = ROOT / 'data'
    output_dir.mkdir(exist_ok=True)

    if args.juz:
        juz_nums = [args.juz]
    else:
        juz_nums = []
        for d in sorted(ROOT.iterdir()):
            m = re.match(r'^juz(\d+)$', d.name)
            if m and (d / 'en').exists() and (d / 'ms').exists():
                juz_nums.append(int(m.group(1)))

    if not juz_nums:
        print('No juzN/ folders with en/ + ms/ found.', file=sys.stderr)
        sys.exit(1)

    for juz_num in juz_nums:
        print(f'Building juz{juz_num}...')
        data = build_juz(juz_num)
        if data is None:
            continue
        out_file = output_dir / f'juz{juz_num}.json'
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        n_sec = len(data['sections'])
        n_toc = len(data['toc'])
        print(f'  → {out_file}  ({n_sec} sections, {n_toc} TOC entries)')


if __name__ == '__main__':
    main()
