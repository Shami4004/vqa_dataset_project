import os
import json
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANGUAGE = "Arabic"  # Change for other batches
taxonomy_path = "../metadata/domain_image_gems.json"  # Update if path differs

def get_image_gems(Physics, Optics, Arabic):
    prompt = f"""
You're helping build a rare image dataset. We need annotated images (text embedded in image) from rare sources.

Return 3–5 rare or underutilized URLs related to:
- Domain: {Physics}
- Subdomain: {Optics}
- Language shown in images: {Arabic}

Return in JSON format:
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
        raw = res.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        print(f"❌ Failed for {domain} > {subdomain}: {e}")
        return []

def enrich_domains(data):
    for domain, subdomains in data.items():
        for subdomain in subdomains:
            if isinstance(subdomains[subdomain], list) and not subdomains[subdomain]:  # only if empty
                print(f"🔍 Enriching: {domain} > {subdomain}")
                sources = get_image_gems(domain, subdomain, LANGUAGE)
                data[domain][subdomain] = sources
                time.sleep(3)

if __name__ == "__main__":
    with open(taxonomy_path, "r") as f:
        data = json.load(f)

    enrich_domains(data)

    with open(taxonomy_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ domain_image_gems.json updated successfully.")