import os
import json
import time
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib.parse

# Load API keys
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Paths
TAXONOMY_PATH = "../metadata/link_dataset.json"
OUTPUT_PATH = "../metadata/arabic_image_links.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

def generate_keywords(domain, subdomain):
    prompt = f"""
Generate 3 to 5 creative Arabic search queries to find image-based resources (illustrations, diagrams, manuscripts) on:
Domain: {domain}
Subdomain: {subdomain}

Return only JSON array like:
["arabic {subdomain.lower()} illustrations", "arabic {subdomain.lower()} historical manuscripts"]
"""

    models = [
        "openai/gpt-3.5-turbo",
        "mistralai/mistral-7b-instruct"
    ]

    for model in models:
        try:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            data = res.json()
            if "choices" not in data:
                print(f"❌ No 'choices' in response:", data)
                continue
            content = data["choices"][0]["message"]["content"].strip()
            return json.loads(content)
        except Exception as e:
            print(f"❌ OpenRouter error ({model}): {e}")
    return []

def google_image_scrape(query, limit=5):
    try:
        search_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.select("img")
        urls = []
        for img in images:
            src = img.get("src")
            if src and "http" in src:
                urls.append(src)
            if len(urls) >= limit:
                break
        return [{"url": url, "desc": f"Image for query: {query}"} for url in urls]
    except Exception as e:
        print(f"❌ Google scrape failed for '{query}':", e)
        return []

def load_taxonomy(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_output(data):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def recursive_enrich(node, path, output):
    for key, value in node.items():
        current_path = path + [key]
        if not value:  # Leaf node
            domain_path = " > ".join(current_path)
            print(f"🔍 Enriching: {domain_path}")

            keywords = generate_keywords(current_path[-2] if len(current_path) > 1 else "", key)
            all_images = []
            for kw in keywords:
                images = google_image_scrape(kw)
                all_images.extend(images)
                time.sleep(1)

            if all_images:
                output[domain_path] = all_images
                print(f"✅ Saved {len(all_images)} images for {domain_path}")
            else:
                print(f"⚠️ No images found for {domain_path}")
        else:
            recursive_enrich(value, current_path, output)

def main():
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    enriched_data = {}
    recursive_enrich(taxonomy, [], enriched_data)
    save_output(enriched_data)
    print("🎉 All done.")

if __name__ == "__main__":
    main()