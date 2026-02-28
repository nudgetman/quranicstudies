# juz8-extended.html — Build Plan

## What I've Learned

### Source Files
- **`juz8.html`** — the template (1,704 lines). Full dark/light themed HTML page with CSS variables, hero section, TOC, passage cards, summary card, and JS theme toggle.
- **`juz8-extended.md`** — the richer content source (1,074 lines). Same 17 passages but with 5–8 scholars per section instead of 3.

### HTML Structure (from juz8.html)
- CSS: theme variables, hero, hero-cards, TOC, surah-banner, passage cards, scholar cards, lessons box, summary card, divider, back-to-top
- Body: hero → info bar → TOC → [surah banner → passage cards] × 2 → divider → summary card → back-to-top
- JS: theme toggle with localStorage

### Content Differences (extended vs. base)
| Feature | juz8.html | juz8-extended.html |
|---|---|---|
| Scholars per passage | 3 | 5–8 |
| Scholars covered | Ibn Kathir, Al-Jalalayn, As-Sa'di | + At-Tabari, Bint Shati', Sayyid Qutb, Ibn Ashur, Yusuf Ali, Abdel Haleem, Muhammad Asad, Sahih International |
| Overview text | Shorter | Richer (with Arabic pronunciations) |
| Key Lessons | Same | Enhanced with Arabic terms |
| Info bar | 3 tafsirs | All 11 scholars |
| Summary card | 9 theme tiles | Same + richer descriptions from MD |
| Scholar Reference Guide | None | Full table at end |

### Keeper items (unchanged)
- "Ramadan 2026" in the gold hero card
- "Nabila" as the reader name
- All Arabic text (identical across both files)
- Same 17 passage sections and all IDs/anchors
- Same CSS (plus small additions for table)

---

## TODO

- [ ] Create `juz8-extended.html` based on `juz8.html` template
- [ ] Update `<title>` to "Juz 8 — Extended Tafsir Guide | Ramadan 2026"
- [ ] Add CSS for scholar reference table (`.scholar-ref-table`)
- [ ] Update info bar to list all 11 scholars
- [ ] Update localStorage key to `juz8-extended-theme`
- [ ] For each of the 17 passages, add expanded scholar cards:
  - [ ] 6:111–121 → add At-Tabari, Bint Shati', Yusuf Ali, Abdel Haleem
  - [ ] 6:122–129 → add At-Tabari, Bint Shati', Sayyid Qutb, Yusuf Ali
  - [ ] 6:130–140 → add At-Tabari, Muhammad Asad, Sahih International
  - [ ] 6:141–150 → add At-Tabari, Bint Shati', Abdel Haleem
  - [ ] 6:151–153 → add At-Tabari, Bint Shati', Ibn Ashur, Yusuf Ali
  - [ ] 6:154–157 → add At-Tabari, Bint Shati', Abdel Haleem
  - [ ] 6:158–165 → add At-Tabari, Sayyid Qutb, Ibn Ashur
  - [ ] 7:1–10    → add At-Tabari, Bint Shati', Muhammad Asad
  - [ ] 7:11–25   → add At-Tabari, Bint Shati', Abdel Haleem
  - [ ] 7:26–43   → add At-Tabari, Bint Shati', Yusuf Ali
  - [ ] 7:44–53   → add At-Tabari, Bint Shati', Muhammad Asad
  - [ ] 7:54–58   → add At-Tabari, Bint Shati', Abdel Haleem
  - [ ] 7:59–64   → add At-Tabari, Bint Shati', Sahih International
  - [ ] 7:65–72   → add At-Tabari, Bint Shati'
  - [ ] 7:73–79   → add At-Tabari, Bint Shati', Yusuf Ali
  - [ ] 7:80–84   → add At-Tabari, Bint Shati'
  - [ ] 7:85–87   → add At-Tabari, Bint Shati', Ibn Ashur, Yusuf Ali
- [ ] Add Scholar Reference Guide section after summary card (markdown table → HTML table)
- [ ] Close closing dua from MD as a footer note

---

## Notes
- Content for each extended scholar card is in `juz8-extended.md` — faithfully transfer, don't paraphrase
- Arabic pronunciation guides in parentheses should be kept in the scholar card text
- The file will be large (~2,500–3,000 lines) — write it in one pass
