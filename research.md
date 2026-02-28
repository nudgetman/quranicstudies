# Quran Research Guide — Format & Scholar Reference

> *This file defines the standard document format and scholar profiles used across all juz research in this project. Reference it when producing any new juz tafsir guide.*

---

## Document Format

Every juz guide follows this structure exactly. Use it as a checklist.

---

### 1. Document Header

```
# Juz [N] — Tafsir Guide

> بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
>
> *A verse-by-verse journey through the [ordinal] portion of the Noble Qur'an*

---

**📗 Surahs covered:** [Surah Name] ([number]:[verses]) & [Surah Name] ([number]:[verses])
**🕌 Revelation:** Makkan / Madinan / Mixed
**📜 Primary Tafsirs:** Ibn Kathir · Al-Jalalayn · As-Sa'di · At-Tabari · Bint Shati'
**📚 Additional Translations & Commentaries:** Yusuf Ali · Sahih International · M.A.S. Abdel Haleem · Muhammad Asad · Sayyid Qutb · Ibn Ashur
```

Always include the Arabic pronunciation note block after the header:

```
> **A Note on Arabic Pronunciations**
> Arabic terms are followed by pronunciation guides in parentheses using approximate English
> phonetics and/or IPA where helpful. Emphasis is marked with **bold** syllables. The letter
> *ʿayn* (ع) is marked as /ʕ/ — a deep throat constriction with no English equivalent.
> The letter *ghayn* (غ) is similar to a French *r*. *Qaf* (ق) is a deep *k* from the back
> of the throat.
```

---

### 2. Table of Contents

Group anchors by Surah. Each entry links to its section anchor.

```
## Table of Contents

### Surah [Name] ([number]) — Verse [range]
- [[verses] — [Section Title]](#anchor-id)

### Surah [Name] ([number]) — Verse [range]
- [[verses] — [Section Title]](#anchor-id)
```

Anchor IDs use the format: first surah sections = `an` + start verse (e.g. `#an111`), second surah = `af` + start verse (e.g. `#af1`). Adjust prefix per surah abbreviation.

---

### 3. Surah Introduction Banner

```
# Surah [Name] (سُورَةُ ...)

**[Name] — [English meaning]**
*[Makkan/Madinan] · [N] verses · [One notable fact about this surah]*

[2–3 sentence introduction: theological character, position in the Qur'an, what this juz
covers within it, and why it matters.]
```

---

### 4. Passage Section (repeat for each passage)

This is the core unit. Every passage follows this exact structure:

```markdown
## [verses] — [Section Title] {#anchor-id}

### Arabic & Translation

> **[Arabic text — key verse(s)]**
>
> *"[English translation]"* — [reference e.g. 6:111]

> **[Arabic text — second key verse if needed]**
>
> *"[English translation]"* — [reference]

### Overview

[2–4 paragraphs of contextual explanation. Include:
- What the passage is about and why it matters
- Key Arabic terms with pronunciation guides in parentheses: **term** (/pronunciation/ — *meaning*)
- Theological or historical context
- Connection to surrounding passages]

---

### 📖 Tafsir Ibn Kathir
[Commentary — typically 2–4 sentences. Focus on: hadith cited, historical context,
specific opinions of companions, theological rulings.]

### 📖 Tafsir Al-Jalalayn
[Commentary — typically 2–3 sentences. Focus on: linguistic meaning of key terms,
classical concise interpretation, legal notes.]

### 📖 Tafsir As-Sa'di
[Commentary — typically 2–3 sentences. Focus on: practical lessons, spiritual
reflection, contemporary relevance, Hanbali legal notes.]

### 📖 Tafsir At-Tabari
[Commentary — typically 3–5 sentences. Focus on: isnād-based narrations from
companions and successors, linguistic analysis, cataloguing of early scholarly opinions,
his own preferred view. Include his full methodological notes where significant.]

### 📖 Bint Shati' (ʿAisha ʿAbd al-Rahman)
[Commentary — typically 3–5 sentences. Focus on: literary-stylistic analysis,
semantic fields, Qur'anic vocabulary across chapters, grammatical structures,
the oral/rhetorical dimension of the text.]

### 📖 Sayyid Qutb (Fi Zilal al-Qur'an)  [include where thematically relevant]
[Commentary — typically 2–4 sentences. Focus on: sociopolitical reading,
the believer's relationship with society, spiritual atmosphere of the passage.]

### 📖 Ibn Ashur (Maqasid Approach)  [include where thematically relevant — especially ethics/law passages]
[Commentary — typically 3–5 sentences. Focus on: maqāṣid al-sharīʿa framework,
objectives of Islamic law, civilisational/social implications.]

### 📖 Yusuf Ali  [include where thematically relevant]
[Commentary — typically 2–3 sentences. Focus on: comparative religious references,
lyrical commentary, English literary framing of Qur'anic imagery.]

### 📖 M.A.S. Abdel Haleem  [include where thematically relevant]
[Commentary — typically 2–3 sentences. Focus on: translation nuances, rhetorical
devices named and explained, accessible modern commentary.]

### 📖 Muhammad Asad (The Message of the Qur'an)  [include where thematically relevant]
[Commentary — typically 2–3 sentences. Focus on: rationalist philosophical reading,
linguistic-philosophical notes, engagement with modernity.]

### 📖 Sahih International  [include where thematically relevant]
[Commentary — typically 1–2 sentences. Focus on: precise modern English rendering,
brief theological clarifications in footnotes.]

---

### ✨ Key Lessons

- [emoji] [Lesson — include key Arabic term with pronunciation where relevant]
- [emoji] [Lesson]
- [emoji] [Lesson]
- [emoji] [Lesson]
- [emoji] [Lesson]

---
```

**Minimum scholars per passage:** Ibn Kathir, Al-Jalalayn, As-Sa'di, At-Tabari, Bint Shati' (5).
**Target scholars per passage:** 5–8, selecting the most thematically relevant additional voices.

---

### 5. Overarching Themes Section

```markdown
# Juz [N] — Overarching Themes

## [emoji] [Theme Name] ([Arabic term])
**[Arabic term]** (/pronunciation/ — *meaning*): [2–3 sentence description of how this theme runs through the Juz.]

## [emoji] [Theme Name]
[Description]

[...repeat for 6–10 themes...]
```

---

### 6. Scholar Reference Guide (closing table)

Always end with this table (static — same for every juz):

```markdown
## Scholar Reference Guide

| Scholar | Period | School/Method | Key Work |
|---|---|---|---|
| **Ibn Kathir** (ابن كثير) | 1301–1373 CE | Athari, Hadith-based | *Tafsīr al-Qurʾān al-ʿAẓīm* |
| **Al-Jalalayn** (الجلالين) | Two scholars, 15th c. | Classical, concise | *Tafsīr al-Jalālayn* |
| **As-Saʿdi** (السعدي) | 1889–1956 CE | Hanbali, practical | *Taysīr al-Karīm al-Raḥmān* |
| **At-Tabari** (الطبري) | 839–923 CE | Traditionalist, encyclopedic | *Jāmiʿ al-Bayān* |
| **Bint Shatiʾ** (بنت الشاطئ) | 1913–1998 CE | Literary-stylistic | *Al-Tafsīr al-Bayānī* |
| **Sayyid Qutb** (سيد قطب) | 1906–1966 CE | Social/political | *Fī Ẓilāl al-Qurʾān* |
| **Ibn Ashur** (ابن عاشور) | 1879–1973 CE | Maqāṣid, objectives | *Al-Taḥrīr wa-l-Tanwīr* |
| **Yusuf Ali** (يوسف علي) | 1872–1953 CE | English, comparative | *The Holy Qurʾan: Text, Translation and Commentary* |
| **Abdel Haleem** (عبد الحليم) | b. 1930 CE | Oxford, accessible English | *The Qurʾan: A New Translation* (Oxford) |
| **Muhammad Asad** (محمد أسد) | 1900–1992 CE | Rationalist, philosophical | *The Message of the Qurʾān* |
| **Sahih International** | 1997 CE | Modern, precise English | *The Qurʾan: Sahih International* |
```

---

### 7. Closing Dua

```markdown
---

*بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ — In the Name of Allah, the Most Gracious, the Most Merciful*

*May Allah make the Qur'an a spring for our hearts, a light for our chests, a remover of our sorrow and a departure of our anxiety. Ameen.*
```

---

## Scholar Profiles

Detailed notes on each scholar's methodology, voice, and what to look for in their commentary.

---

### Ibn Kathir (ابن كثير)
**Full name:** Ismail ibn Umar ibn Kathir al-Qurashi
**Period:** 1301–1373 CE (701–774 AH)
**School:** Athari (traditionalist); student of Ibn Taymiyyah
**Key work:** *Tafsīr al-Qurʾān al-ʿAẓīm* (*Tafsir of the Great Qur'an*)
**Method:** Tafsir by Qur'an first (cross-referencing verses), then by hadith, then by companion opinions. Prioritises authentic narrations over rational speculation.
**Voice in commentary:** Historical, hadith-citing, authoritative. Mentions specific companions (ʿUmar, Ibn ʿAbbas), cites chains of narration, gives legal rulings where relevant.
**Best for:** Theological rulings, hadith support, historical context, companion opinions, stories of previous nations (qiṣaṣ al-anbiyāʾ).

---

### Al-Jalalayn (الجلالين)
**Full name:** Two scholars — Jalal al-Din al-Mahalli (1389–1459 CE) and his student Jalal al-Din al-Suyuti (1445–1505 CE)
**Period:** 15th century CE
**School:** Shafi'i; classical Ash'ari
**Key work:** *Tafsīr al-Jalālayn* (*Tafsir of the Two Jalals*)
**Method:** Concise word-by-word and phrase-by-phrase classical interpretation. One of the most widely taught tafsirs in traditional Islamic education.
**Voice in commentary:** Brief, precise, lexical. Explains grammatical structures, defines key words, gives the orthodox classical reading without extended discussion.
**Best for:** Clean classical meaning of words and phrases; standard legal/theological positions; baseline interpretation to anchor other commentaries.

---

### As-Sa'di (السعدي)
**Full name:** Sheikh ʿAbd al-Rahman ibn Nasir al-Saʿdi
**Period:** 1889–1956 CE
**School:** Hanbali; influenced by Ibn Taymiyyah and Ibn al-Qayyim
**Key work:** *Taysīr al-Karīm al-Raḥmān fī Tafsīr Kalām al-Mannān* (*Facilitation of the Most Gracious*)
**Method:** Practical and accessible; focuses on deriving spiritual, ethical, and practical lessons. Less hadith-heavy than Ibn Kathir; more reflective.
**Voice in commentary:** Warm, direct, lesson-oriented. Speaks to the believer's heart. Often draws contemporary applications and spiritual reflections.
**Best for:** Practical lessons, spiritual dimension, ethical applications, accessible theology, heart-centred reflection.

---

### At-Tabari (الطبري)
**Full name:** Muhammad ibn Jarir al-Tabari
**Period:** 839–923 CE (224–310 AH) — the earliest of the major tafsir scholars
**School:** Founded his own school of jurisprudence (later dissolved); Traditionalist/Athari in creed
**Key work:** *Jāmiʿ al-Bayān ʿan Taʾwīl Āy al-Qurʾān* (*The Comprehensive Exposition of the Interpretation of the Verses of the Qur'an*) — 30 volumes
**Method:** Encyclopedic collection of all available early opinions, each with isnād (chain of transmission). Provides linguistic analysis, catalogues every significant early scholarly position, then usually states his own preferred view.
**Voice in commentary:** Scholarly, thorough, historically grounded. Frequently says "the correct view is…" after presenting multiple positions. Provides linguistic etymology of key terms.
**Best for:** Early scholarly diversity of opinion, linguistic analysis of specific Arabic terms, historical context, seeing the full range of classical interpretations before they were narrowed by later tradition.

---

### Bint Shati' (بنت الشاطئ)
**Full name:** ʿAisha ʿAbd al-Rahman
**Pen name:** Bint Shati' (*Daughter of the Riverbank*)
**Period:** 1913–1998 CE
**School:** Egyptian literary-stylistic; groundbreaking 20th-century female scholar
**Key work:** *Al-Tafsīr al-Bayānī lil-Qurʾān al-Karīm* (*The Literary Exposition of the Noble Qur'an*)
**Method:** Analyses the Qur'an as a unified literary text. Studies: word choice across chapters (semantic fields), grammatical structures and their theological significance, rhetorical devices (iltifāt, istifhām inkārī, etc.), the oral/phonetic dimension of the text.
**Voice in commentary:** Precise, literary, sometimes striking. Points out things no other classical commentator noticed — e.g. the use of dhālika vs. hādhā, grammatical person shifts, recurring vocabulary networks.
**Best for:** Literary analysis, Qur'anic rhetoric, semantic fields across chapters, how the form of the Arabic itself carries theological meaning, unique female scholarly voice.
**Key concepts she uses:**
- **Iltifāt** (/ˌil.ti.ˈfaːt/) — grammatical person shift (1st → 3rd → 2nd person) for rhetorical effect
- **Istifhām inkārī** (/ˌis.tiˈfhaːm ˌin-ˈkaː-riː/) — rhetorical disapproving interrogative
- **Istiʿāra** (/ˌis-tiˈʕaː-ra/) — metaphor (she identifies sustained metaphors across chapters)
- **Semantic fields** — recurring word-families that build a unified theological vocabulary

---

### Sayyid Qutb (سيد قطب)
**Full name:** Sayyid Qutb Ibrahim Husayn Shadhili
**Period:** 1906–1966 CE (partly written from prison in Egypt)
**School:** Egyptian; influenced by Mawdudi; later developed his own framework
**Key work:** *Fī Ẓilāl al-Qurʾān* (*In the Shade of the Qur'an*) — 30 volumes, written partly in prison
**Method:** Spiritual-experiential and sociopolitical. Reads the Qur'an as speaking directly to the modern believer's situation — oppression, corrupted societies, the struggle to live by divine guidance.
**Voice in commentary:** Passionate, evocative, sometimes urgent. Strong aesthetic sense — describes the "atmosphere" of surahs. Politically charged but deeply spiritual. Use his insights on spiritual atmosphere and social critique; treat his political conclusions with scholarly caution.
**Best for:** Spiritual atmosphere of passages, sociopolitical reading of prophetic narratives, the believer's psychology under pressure, eschatological passages, the aesthetics of Qur'anic narrative.
**Key concept:** **Ḥākimiyya** (/ħaː.ki.ˈmij.ja/) — sovereignty belongs to Allah alone; any human authority is a delegated, accountable stewardship.

---

### Ibn Ashur (ابن عاشور)
**Full name:** Muhammad al-Tahir ibn Ashur
**Period:** 1879–1973 CE
**School:** Maliki; Tunisian; Grand Mufti and Rector of Zaytuna University
**Key work:** *Al-Taḥrīr wa al-Tanwīr* (*Liberation and Enlightenment*) — 30 volumes
**Method:** Applies the **maqāṣid al-sharīʿa** (objectives of Islamic law) framework to tafsir. Also provides rigorous linguistic analysis. Bridges classical scholarship and modern engagement with Islamic civilisation.
**Voice in commentary:** Structured, intellectually rigorous, civilisational in scope. Often identifies the social purpose of a command or narrative, not just its surface meaning.
**Best for:** Legal and ethical passages, the social/civilisational dimension of Islamic commands, the "why" behind rulings, connecting Qur'anic values to institutional and social structures.
**Key concept:** **Maqāṣid al-sharīʿa** (/ma.ˈqaː.sid aʃ-ʃaˈriːʕa/) — the six protected interests: religion (dīn), life (nafs), intellect (ʿaql), progeny (nasl), wealth (māl), honour (ʿirḍ).

---

### Yusuf Ali (يوسف علي)
**Full name:** Abdullah Yusuf Ali
**Period:** 1872–1953 CE
**School:** Indian-British; comparativist; classical education + Western academic training
**Key work:** *The Holy Qur'an: Text, Translation and Commentary*
**Method:** Lyrical English translation with extensive footnotes. Draws on comparative religion (Bhagavad Gita, Bible, Stoics), history, and classical Islamic scholarship. Bridges Islamic and Western intellectual traditions.
**Voice in commentary:** Eloquent, literary, sometimes poetic. Good for connecting Qur'anic imagery to universal human experience. Translations are sometimes dated but the commentary notes are rich.
**Best for:** English literary framing, comparative religious parallels, historical notes, connecting Qur'anic ethics to universal moral traditions.

---

### M.A.S. Abdel Haleem (عبد الحليم)
**Full name:** Muhammad Abdel Haleem
**Period:** Born 1930 CE; Professor at the School of Oriental and African Studies (SOAS), University of London
**School:** Egyptian-British; academic Islamic studies
**Key work:** *The Qur'an: A New Translation* (Oxford World's Classics)
**Method:** Produces accessible, accurate modern English translations. Commentary focuses on rhetorical devices, translation nuances, and making the Qur'an's argument clear to a modern English reader.
**Voice in commentary:** Clear, precise, academic but accessible. Excellent at naming rhetorical devices and explaining why a particular Arabic construction matters.
**Best for:** Translation nuances, rhetorical analysis, clarifying ambiguous passages, modern English audience accessibility.

---

### Muhammad Asad (محمد أسد)
**Full name:** Muhammad Asad (born Leopold Weiss)
**Period:** 1900–1992 CE; Austrian-born, converted to Islam
**School:** Rationalist-philosophical; heavily influenced by classical Arabic linguistics
**Key work:** *The Message of the Qur'an*
**Method:** Rationalist reading that takes classical Arabic linguistics seriously while engaging with modern thought. Known for sometimes unconventional interpretations grounded in linguistic analysis. Resists literalism where he finds a stronger linguistic case for a different reading.
**Voice in commentary:** Intellectual, sometimes provocative, always linguistically justified. Engages with Western philosophy and sciences. Valuable as a counterpoint; some interpretations are contested.
**Best for:** Linguistic philosophical analysis, engagement with modernity, alternative readings grounded in Arabic etymology, the Qur'an's relationship with human reason.

---

### Sahih International
**Period:** Published 1997
**School:** Salafi-leaning; produced in Saudi Arabia
**Key work:** *The Qur'an: Sahih International*
**Method:** Modern, precise English translation prioritising accuracy and clarity. Footnotes are brief and focused on theological clarification. Avoids interpretive elaboration.
**Voice in commentary:** Neutral, precise, direct. Minimal stylistic flair; maximum accuracy.
**Best for:** Clean modern baseline translation; theological precision on creedal points; brief clarifications of contested terms.

---

## Format Conventions

### Arabic Terms
Always include: **Arabic term** (/IPA or phonetic pronunciation/ — *English meaning*) on first use in a section.
Example: **nūr** (/nuːr/ — *light*), **tawḥīd** (/taw-ˈħiːd/ — *monotheism*)

### IPA Quick Reference
| Arabic letter | Phonetic symbol | Description |
|---|---|---|
| ع (ʿayn) | /ʕ/ | Deep throat constriction |
| غ (ghayn) | /ɣ/ | Like French *r* |
| ق (qaf) | /qˤ/ | Deep *k* from back of throat |
| ح (ha) | /ħ/ | Breathy *h* |
| خ (kha) | /x/ | Like Scottish *loch* |
| ص (sad) | /sˤ/ | Emphatic *s* |
| ض (dad) | /dˤ/ | Emphatic *d* |
| ط (ta) | /tˤ/ | Emphatic *t* |
| ظ (dha) | /ðˤ/ | Emphatic *th* |
| ذ (dhal) | /ð/ | Like *th* in *this* |
| ث (tha) | /θ/ | Like *th* in *think* |

### Passage Grouping
Group 7–12 consecutive verses into one passage section. Each group should have a unified theme or narrative unit. Titles should be evocative, not just verse numbers.

### Emoji Conventions for Key Lessons
Use consistent emoji for recurring themes:
- 🕌 Tawhid / worship
- ⚖️ Justice / accountability
- 💡 Faith / light / guidance
- 🤲 Dua / gratitude / mercy
- 📖 Knowledge / Qur'an
- ❤️ Spiritual transformation
- 😈 Iblis / arrogance / deception
- 🌧️ Rain / revival / mercy
- 👁️ Signs / reflection
- ⏰ Urgency / this life / repentance
- 🏔️ Eschatology / afterlife
- 🤝 Prophets / brotherhood
- ⛵ Community / salvation
- 🌍 Earth / stewardship / khilāfah

---

## Juz Coverage Reference

| Juz | Surahs | Verses | Revelation |
|---|---|---|---|
| 1 | Al-Fatiha 1 + Al-Baqarah 2:1–141 | — | Madinan |
| 2 | Al-Baqarah 2:142–252 | — | Madinan |
| 3 | Al-Baqarah 2:253–286 + Al-Imran 3:1–91 | — | Madinan |
| 4 | Al-Imran 3:92–200 + An-Nisa 4:1–23 | — | Madinan |
| 5 | An-Nisa 4:24–147 | — | Madinan |
| 6 | An-Nisa 4:148–176 + Al-Ma'idah 5:1–81 | — | Madinan |
| 7 | Al-Ma'idah 5:82–120 + Al-An'am 6:1–110 | — | Makkan (An'am) |
| **8** | **Al-An'am 6:111–165 + Al-A'raf 7:1–87** | — | **Makkan** |
| 9 | Al-A'raf 7:88–206 + Al-Anfal 8:1–40 | — | Mixed |
| 10 | Al-Anfal 8:41–75 + At-Tawbah 9:1–92 | — | Madinan |
| 11 | At-Tawbah 9:93–129 + Yunus 10:1–109 + Hud 11:1–5 | — | Mixed |
| 12 | Hud 11:6–123 + Yusuf 12:1–52 | — | Makkan |
| 13 | Yusuf 12:53–111 + Ar-Ra'd 13 + Ibrahim 14 + Al-Hijr 15:1–1 | — | Mixed |
| 14 | Al-Hijr 15 + An-Nahl 16:1–128 | — | Makkan |
| 15 | Al-Isra 17 + Al-Kahf 18:1–74 | — | Makkan |
| 16 | Al-Kahf 18:75–110 + Maryam 19 + Taha 20:1–135 | — | Makkan |
| 17 | Al-Anbiya 21 + Al-Hajj 22:1–78 | — | Mixed |
| 18 | Al-Mu'minun 23 + An-Nur 24 + Al-Furqan 25:1–20 | — | Mixed |
| 19 | Al-Furqan 25:21–77 + Ash-Shu'ara 26 + An-Naml 27:1–55 | — | Makkan |
| 20 | An-Naml 27:56–93 + Al-Qasas 28 + Al-Ankabut 29:1–44 | — | Makkan |
| 21 | Al-Ankabut 29:45–69 + Ar-Rum 30 + Luqman 31 + As-Sajda 32 | — | Makkan |
| 22 | Al-Ahzab 33 + Saba 34 + Fatir 35:1–45 | — | Mixed |
| 23 | Ya-Sin 36 + As-Saffat 37 + Sad 38 + Az-Zumar 39:1–31 | — | Makkan |
| 24 | Az-Zumar 39:32–75 + Ghafir 40 + Fussilat 41:1–46 | — | Makkan |
| 25 | Fussilat 41:47–54 + Ash-Shura 42 + Az-Zukhruf 43 + Ad-Dukhan 44 + Al-Jathiyah 45 | — | Makkan |
| 26 | Al-Ahqaf 46 + Muhammad 47 + Al-Fath 48 + Al-Hujurat 49 + Qaf 50 | — | Mixed |
| 27 | Adh-Dhariyat 51 + At-Tur 52 + An-Najm 53 + Al-Qamar 54 + Ar-Rahman 55 + Al-Waqi'ah 56 + Al-Hadid 57 | — | Makkan/Mixed |
| 28 | Al-Mujadila 58–Al-Tahrim 66 | — | Madinan |
| 29 | Al-Mulk 67–Al-Mursalat 77 | — | Makkan |
| 30 | An-Naba 78–An-Nas 114 | — | Makkan |

*(Juz 8 is complete — see `juz8-extended.md` and `juz8-extended.html`)*

---

## Research Workflow

When asked to research a new juz:

1. **Identify the passages** — look up the juz boundaries, note the surahs and verse ranges
2. **Group into 7–15 passage sections** — each with a unified theme
3. **Write the surah introduction(s)** — character, revelation context, key theological contribution
4. **For each passage:**
   - Write the Arabic text (key representative verses)
   - English translation
   - Overview (2–4 paragraphs)
   - Commentary from each applicable scholar (min. 5: Ibn Kathir, Al-Jalalayn, As-Sa'di, At-Tabari, Bint Shati')
   - Key Lessons (5 bullet points)
5. **Write Overarching Themes** — identify 6–10 major themes running through the juz
6. **Close with Scholar Reference Guide and closing dua**

---

*Reference this file whenever producing a new juz research document.*
