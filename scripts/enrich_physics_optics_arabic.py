import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# Load your .env credentials
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configurable parameters
taxonomy_path = "../metadata/domain_image_gems.json"
LANGUAGE = "Arabic"
DOMAIN = "Physics"
SUBDOMAIN = "Optics"

# --- Helper to extract valid JSON from LLM response ---
def extract_json_block(text):
    try:
        match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("No valid JSON array found in the response.")
    except Exception as e:
        print(f"❌ JSON extraction error: {e}")
        return []

# --- Call Groq API with prompt ---
def get_image_gems(domain, subdomain, language):
    prompt = f"""
You're helping build a rare image dataset. We need annotated images (text embedded in the image) from rare sources.

Return 3–5 rare or underutilized websites, galleries, or archives related to:
- Domain: {domain}
- Subdomain: {subdomain}
- Language shown in images: {language}

Return in JSON format only:
[
  {{
    "url": "https://example.com",
    "desc": "Short description"
  }}
]
"""
    try:
        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = res.choices[0].message.content.strip()
        return extract_json_block(content)
    except Exception as e:
        print(f"❌ Error while fetching image_gems: {e}")
        return []

# --- Update the taxonomy JSON file ---
def update_json_file():
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"🔍 Enriching {DOMAIN} > {SUBDOMAIN} in {LANGUAGE}...")
    image_links = get_image_gems(DOMAIN, SUBDOMAIN, LANGUAGE)

    if image_links:
        if DOMAIN not in data:
            data[DOMAIN] = {}
        if SUBDOMAIN not in data[DOMAIN]:
            data[DOMAIN][SUBDOMAIN] = {}

        # Add language-specific image gems
        data[DOMAIN][SUBDOMAIN][LANGUAGE] = {
            "image_gems": image_links
        }

        with open(taxonomy_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Updated {DOMAIN} > {SUBDOMAIN} in {LANGUAGE}.")
    else:
        print(f"⚠️ No image links returned. Nothing was updated.")

# --- Run script ---
if __name__ == "__main__":
    update_json_file()