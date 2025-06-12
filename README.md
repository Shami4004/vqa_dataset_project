# VQA Dataset Project

This project prepares a multilingual dataset of images containing embedded text for Visual Question Answering (VQA) tasks.

## Structure

- `raw_images/`: Downloaded image files by domain & language
- `metadata/`: JSON files containing image metadata
- `scripts/`: Scraping & metadata generation scripts
- `logs/`: Logging directory (optional)

## Scripts

- `image_scraper.py`: Scrapes images using DuckDuckGo and generates metadata
- `generate_metadata.py`: Regenerates metadata from existing image folders