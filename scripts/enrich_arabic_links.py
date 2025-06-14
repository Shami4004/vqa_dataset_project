import os
import json
import requests
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

LINK_DATASET_PATH = "../metadata/link_dataset.json"
OUTPUT_PATH = "../metadata/domain_image_gems_arabic.json"

# OpenRouter Keyword Generator
def generate_keywords(domain, subdomain):
    prompt = f"""You are helping build a rare Arabic image dataset.
Suggest 3–5 search keywords in English that could retrieve Arabic-language diagrams or illustrations related to:

- Domain: {domain}
- Subdomain: {subdomain}

The output must be a JSON list like:
["Arabic optics manuscript", "historical Arabic physics diagrams", "Islamic optics texts"]"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content.strip())
    except Exception as e:
        print(f"❌ OpenRouter error for {domain} > {subdomain}: {e}")
        return []

# SerpAPI Image Fetcher
def fetch_images_from_serpapi(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_KEY
        }
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        images = response.json().get("images_results", [])[:5]
        return [{"url": img["original"], "desc": f"Image for query: {query}"} for img in images]
    except Exception as e:
        print(f"❌ SerpAPI error for '{query}': {e}")
        return []

# Recursive Enrichment
def enrich_links(data, out_data, path=[]):
    for key, value in data.items():
        if isinstance(value, dict) and value == {}:
            domain, subdomain = path[0], " > ".join(path[1:] + [key])
            print(f"🔍 {domain} > {subdomain}")

            keywords = generate_keywords(domain, subdomain)
            images = []
            for kw in keywords:
                images.extend(fetch_images_from_serpapi(kw))

            # Create nested path
            curr = out_data
            for p in path + [key]:
                curr = curr.setdefault(p, {})
            curr["image_gems"] = images

        elif isinstance(value, dict):
            enrich_links(value, out_data, path + [key])

def main():
    with open(LINK_DATASET_PATH, "r", encoding="utf-8") as f:
        link_data = json.load(f)

    enriched_data = {}
    enrich_links(link_data, enriched_data)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Arabic enrichment complete → {OUTPUT_PATH}")

if __name__ == "__main__":
    main()