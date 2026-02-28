# Slug-based Routing: `/{lang}/juz{N}`
## Problem
Juz pages currently use URL parameters (`juz-page.html?juz=2`) and language is managed purely client-side via localStorage. The goal is clean slug URLs like `/en/juz1`, `/ms/juz2#section-02`.
## Current State
* `serve.sh` runs `python3 -m http.server 8080` (no routing support)
* `juz-page.html` reads `?juz=N` from URL params, fetches `data/juzN.json`, language from localStorage
* `index.html` links use a mix of `juz-page.html?juz=N` and `juzN.html`
* Language toggle re-renders in place, no URL change
## Proposed Changes
### 1. Custom Python server (`server.py`)
Replace `serve.sh` / plain `http.server` with a lightweight custom handler:
* Requests matching `/{lang}/juz{N}` (e.g. `/en/juz2`, `/ms/juz14`) serve the template HTML file (`juz-page.html`)
* All other requests (static files like `/data/juz2.json`, `/index.html`, `/`) served normally
* Update `serve.sh` to run `python3 server.py` instead
### 2. Modify `juz-page.html` — path-based routing
Replace the URL-parameter boot logic with path parsing:
* Parse `window.location.pathname` to extract `lang` and `juzNum`:
    * `/en/juz2` → `lang='en'`, `juzNum='2'`
* Set initial `LANG` from URL path instead of localStorage
* Fetch data the same way: `data/juz{N}.json` (use absolute path `/data/juz{N}.json` so it works from any route)
* Anchor scrolling (`#section-02`) continues to work with no changes
### 3. Language toggle → URL navigation
Instead of just re-rendering in place, the language toggle should:
* Update the URL using `history.replaceState` to `/{newLang}/juz{N}` (keeps same hash/anchor)
* Re-render the page (no reload needed)
* Still save preference to localStorage for the index page
### 4. Update `index.html` links
* All juz card `href` values change to `/en/juz{N}` (e.g. `/en/juz1`, `/en/juz2`, ...)
* The default language in links is `en`; once on a juz page, user can toggle to `ms`
* Coming-soon cards remain disabled (`pointer-events: none`) but still use the new URL pattern
### 5. Delete `juz-page.html`?
No — `juz-page.html` stays as the template file served by the custom server. It is no longer accessed directly by users, but the server returns its contents when a `/{lang}/juz{N}` route is hit. We can rename it to `_juz-template.html` (prefixed with underscore) to make this clearer, but this is optional.
## Files Changed
* **`server.py`** — new custom server
* **`serve.sh`** — update to run `server.py`
* **`juz-page.html`** — replace URL param logic with path parsing, update fetch URL, update language toggle
* **`index.html`** — update all juz card hrefs
