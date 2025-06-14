
## 🔍 Rare Image Scraping & Sourcing Strategy for VQA (Ultra-Detailed Version)

**Context & Taxonomy**

* JSON taxonomy loaded via `taxonomy.json`.
  For now, it is exhaustive and will serve as our base.

---

### 1. Examples of Manually Curated Sources – Zero Authentication Catalog

Each source listed below is freely accessible (no API key, no login), and covers niches that are rarely indexed.
We’ll enrich it by theme according to `taxonomy.json`.

| # | Theme                              | Endpoint / URL                                                                                   | Parameters & Tips                                       | Key Metadata                            |
| - | ---------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | --------------------------------------- |
| 1 | **Astronomy & Satellite**          | `https://images-assets.nasa.gov/image/<nasa_id>/collection.json`                                 | Implicit pagination: increment `<nasa_id>`              | `nasa_id`, `date_created`, `instrument` |
| 2 | **Geology & Natural Environments** | `https://geoserver.example.gov/ows?service=WMS&request=GetMap&LAYERS=rock_core&FORMAT=image/png` | BBOX + `WIDTH=2048&HEIGHT=2048`                         | `layer`, `bbox`, `timestamp`            |
| 3 | **Cultural Heritage**              | `https://gallica.bnf.fr/ark:/12148/{ark_id}/f1.json`                                             | `ark_id` listed via `catalog/search?q=iconography`      | `ark_id`, `year`, `collection`          |
| 4 | **Historical Maps**                | `https://maps.nypl.org/warper/maps/<map_id>/export?format=jpg`                                   | Extract `<map_id>` from HTML page                       | `map_id`, `title`, `georeference`       |
| 5 | **Open Medical Images**            | `https://openprescribing.net/media/images/<year>/<month>.zip`                                    | Monthly ZIP files, extract JPG >1200×1200 px            | `year`, `month`, `filename`             |
| 6 | **Scientific Illustrations**       | `https://journals.plos.org/plosone/article/file?id={doi}&type=printable`                         | Extract figures from PDF, parse XObjects via `pdfminer` | `doi`, `figure_label`, `caption`        |
| 7 | **Open Maps**                      | `https://tile.openstreetmap.org/{z}/{x}/{y}.png`                                                 | Zoom 15–18, convert PNG→JPEG high quality               | `z`, `x`, `y`, `timestamp`              |
| 8 | **Digital Library**                | `https://gallica.bnf.fr/ark:/12148/<ark_id>/f2.highres`                                          | Add `/f2.highres` to get high-def version               | `ark_id`, `resolution`, `size`          |
| 9 | **Historic PDFs**                  | `https://archive.org/download/<collection>/<file>.pdf`                                           | List `<collection>` via search, extract images          | `collection`, `file`, `page`            |

> **Rare Tip**: Some sites hide subdomains (e.g. `media1.gallica.bnf.fr`). Scan subdomains via `domaincrawl` to multiply endpoints.

---

### 2. Technical Pipeline – Granularity & Hidden Tips

Project tree (open source stack):

```
scraper_project/
├── config/                # TOML + YAML (throttle, endpoints)
├── taxonomy_loader.py     # JSON -> Python objects
├── source_registry.yaml   # source list, filters, schedule
├── spiders/               # Scrapy + Selenium HEADLESS
├── utils/                 # watermark_detector.py, ocr_filter.py
├── pipelines/             # extract, filter, metadata_encode
├── orchestrator/          # Airflow scripts (or simple cron)
└── main.py                # Minimal CLI -> triggers
```

P.S: Don’t hesitate to change this. I generated it with AI. Make your own or improve this example.
**2.1 Registry & Scheduling**

* **YAML** defines for each source: `interval=24h`, `window=02:00-04:00 CET`, `parallel=5`.
* **Tip**: isolate heavy scrapes (PDF, WMS) to off-peak windows, stay under 50 requests/minute.

**2.2 Scrapy Spiders**

* **BaseSpider**: handles pagination, 5xx errors, `retry=3`, exponential backoff.
* **Middlewares**:

  * **Proxy Rotation**: `free-proxy` pool + direct fallback.
  * **User-Agent Pool**: custom list + `fake_useragent`.
* **JS Extraction**: Selenium HEADLESS + `--disable-blink-features=AutomationControlled`.

  * **Tip**: load pre-generated cookies via `requests` to avoid CAPTCHA.

**2.3 Filtering & Quality**

* **Resolution**: always fetch the best quality.
  Example config: (min 800×800→1200×1200 based on category).
* **Watermark**: `utils/watermark_detector.py` (light CNN) detects with >85% precision (up to you).
* **OCR**: `utils/ocr_filter.py` (Tesseract), rejects if >20% of pixels contain text.
* **Tip**: for maps, use `gdal_translate -scale` to normalize range before filtering. (if too complex, skip it or avoid downloading multispectral maps with more than 3 bands)

**2.4 Metadata & Enrichment**

* **Local tagging**: YOLOv5 (Docker) for basic classification (architecture, diagram,…)

**2.5 Free Storage**

* **Google Drive**: `gdrive-cli` → folder `/VQA_Raw/YYYY-MM-DD/`
* **GitHub**: push `metadata.json` + small samples (≤50 KB) to `repo/vqa-daily`
* **Slack**: upload thumbnails + JSON report via `#vqa-report` webhook

**2.6 Simple Orchestration**

* **Cron + Makefile**: hourly crons for each step, logs in `logs/`.
* **Tip**: to re-trigger a blocked extraction, use `make retry SOURCE=<source_name>`

---

---

**Project Milestones for the Next 10 Days (Improve this)**

Each milestone must be locked by midnight CET. Any delay triggers immediate escalation on Slack (#vqa-escalation).

* **D+1 (June 15, 11:59 PM CET)**

  * 📑 Finalize `source_registry.yaml` for all level 1 and 2 taxonomies (`Sciences`, `Tech`, `Social Sciences`, etc.)
  * ✅ Validate 100% of listed endpoints (ping 200 OK)
* **D+2 (June 16, 11:59 PM CET)**

  * 🕷️ Deploy 5 Scrapy spiders covering 3 distinct themes (e.g. `Astronomy`, `Biology`, `History`)
  * 🔄 Robustness test: each spider must handle 5× 5xx errors without crashing
* **D+3 (June 17, 11:59 PM CET)**

  * 🧹 `filter_pipeline.py` operational for these 5 spiders (resolution and watermark filtering)
  * 🔍 Auto quality report: rejection rate <20% per spider
* **D+4 (June 18, 11:59 PM CET)**

  * 🛠️ Integrate `metadata.py`: extract DOI/EXIF/ark\_id for each image
  * 🏷️ Generate `metadata_YYYYMMDD.json` with 10 valid examples per source
* **D+5 (June 19, 11:59 PM CET)**

  * 🚀 Automate `github_push.sh`: auto PR created with metadata + 10 thumbnails (≤20 KB)
  * 📌 Check GitHub Actions CI (workflow `daily-scrape`) passes green
* **D+6 (June 20, 11:59 PM CET)**

  * 📂 Deploy Drive upload (`upload_drive.sh`): folder `/VQA_Raw/YYYY-MM-DD/` contains ≥50 images
  * 🔔 Post Slack report via webhook, include stats and Drive links
* **D+7 (June 21, 11:59 PM CET)**

  * 🔄 Full loop tested: scrape → filter → metadata → GitHub → Drive → Slack without intervention
  * 📊 Simplified dashboard in README.md (terminal-style table)
* **D+8 (June 22, 11:59 PM CET)**

  * ⚙️ Add retry system (`make retry`) for blocked sources (backoff logic)
  * 📝 Document common errors + fixes in `docs/troubleshooting.md`
* **D+9 (June 23, 11:59 PM CET)**

  * 🧪 Write 5 unit tests for `utils/watermark_detector.py` and `ocr_filter.py`
  * ✅ Coverage >80% for these modules
* **D+10 (June 24, 11:59 PM CET)**

  * 🤖 Set up GitHub Actions regression checks for full pipeline
  * 🚨 Auto-escalation if `daily-scrape` workflow fails

> *Every evening at 6:00 PM CET, short stand-up (10 min) on #vqa-standup — blockers, next-day priorities.*

