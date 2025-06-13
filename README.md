# 🧠 VQA Dataset Project

This project aims to build a multilingual, multi-domain Visual Question Answering (VQA) dataset. It is structured on a rich taxonomy, populated with images from rare and underutilized sources, and annotated with high-quality visual reasoning questions.

---

## 🔍 Data Sourcing Philosophy

Unlike generic scraping from Google or Bing, we focus on:
- Academic journals and institutional archives
- Language-specific content (Arabic, Korean, Japanese, etc.)
- Open government repositories
- Niche forums and deep search platforms (Windsurf, Cursor, DeepSearch)

Each image must:
- Contain text **within the image**
- Avoid watermarks or copyright issues
- Be visually and semantically relevant to the assigned domain/subdomain

---

## 🗂️ Project Structure
vqa_dataset_project/
├── raw_images/                 # Downloaded images by domain/subdomain
│   └── [domain]/[subdomain]/[theme]/image.jpg
├── metadata/                  # Taxonomy & image metadata
│   └── taxonomy_structure.json
├── qa_data/                   # VQA JSONL outputs
│   └── [domain]_[subdomain].jsonl
├── scripts/                   # Scraper & processing tools
│   ├── image_scraper.py
│   ├── generate_metadata.py
├── README.md

---

## 📄 JSONL Output Format

Each image entry includes 5 diverse reasoning questions:
- Object recognition
- Causal/logical inference
- Intermodal (e.g., MRI, satellite)
- Color-based reasoning
- Spatial awareness

```json
{
  "image_id": "medical_001",
  "image_path": "images/medicine/radiology/brain_scan/medical_001.jpg",
  "domain": "medicine",
  "subdomain": "radiology",
  "theme": "brain_scan",
  "language": "en",
  "image_metadata": {
    "width": 1024,
    "height": 768,
    "format": "JPEG"
  },
  "questions": [
    {
      "question": "What part of the brain is shown?",
      "answer": "Frontal lobe",
      "type": "object_recognition",
      "difficulty": "medium"
    }
    // ...4 more types
  ]
}