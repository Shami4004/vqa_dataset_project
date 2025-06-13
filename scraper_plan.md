# 🔍 Scraper Plan & Rare Image Sourcing Strategy

This document outlines the strategy for sourcing high-quality and rare images that match our Visual Question Answering (VQA) taxonomy. The goal is to avoid scraping from overused search engines and instead focus on lesser-known, high-value sources.

---

## 🎯 Strategy Summary

We will source images from:

1. **Manually Curated Archives**
   - Government and NGO data portals
   - Academic journal image sections
   - Language-specific sites (Korean, Japanese, Arabic)

2. **Deep Web Tools & Agents**
   - Cursor (for code-based assistance)
   - Windsurf (deep search AI)
   - DeepSearch via OpenAI API

3. **Fallback Methods**
   - DuckDuckGo + careful filters
   - Direct web scraping (via `requests`, `bs4`)
   - Public datasets like Flickr Commons

---

## 🌍 Rare Sources To Explore

| Source | Use Case |
|--------|----------|
| [commons.wikimedia.org](https://commons.wikimedia.org) | Visual arts, history, science |
| [pubs.rsna.org](https://pubs.rsna.org) | Radiology images |
| [data.nasa.gov](https://data.nasa.gov) | Satellite, engineering |
| [www.jstage.jst.go.jp](https://www.jstage.jst.go.jp) | Japanese research visuals |
| [apps.who.int/iris](https://apps.who.int/iris) | Medical/health posters in multiple languages |
| [flickr.com/commons](https://flickr.com/commons) | Crowd-sourced cultural data |
| [www.loc.gov](https://www.loc.gov) | Library of Congress |
| [digital.library.villanova.edu](https://digital.library.villanova.edu) | Historical illustrations |
| [koreascience.or.kr](https://koreascience.or.kr) | Korean domain-specific images |
| [openei.org](https://openei.org) | Environmental engineering visuals |

---

## 🛠️ Scraping Tools & Techniques

| Tool | Purpose |
|------|---------|
| `requests`, `BeautifulSoup` | HTML scraping |
| `duckduckgo_search` | Lightweight image scraping |
| `Pillow`, `tqdm` | Image handling and tracking |
| Cursor / Windsurf | Suggest niche sources via agents |

---

## 📎 Notes

- All sources will be documented with URL and use-case.
- Images with watermarks or external text layers will be rejected.
- Language-specific filters will be applied based on theme/domain.

---

## ✅ Output Format

Each day, we will create:
- A list of links used
- Image metadata per file
- Verified subdomain folders
- Daily delivery in Google Drive