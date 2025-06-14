import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Editable parameters
TAXONOMY_PATH = "./domain_image_gems.json"
LANGUAGE = "Arabic"
DOMAIN = "Physics"
SUBDOMAIN = "Optics"

# Prompt to get creative keyword ideas
def get_search_prompt(domain, subdomain, language):
    return f"""
You're helping build a rare image dataset. Suggest 5 creative and unusual image search keyword ideas for:

- Domain: {domain}
- Subdomain: {subdomain}
- Language: {language}

Output JSON list like:
["Arabic optics manuscripts", "Ibn al-Haytham diagrams", "historical physics scrolls in Arabic"]
"""

# Use OpenRouter to generate keyword list
def fetch_keywords_from_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    models = [
        "openchat/openchat-3.5-0106",
        "openai/gpt-3.5-turbo"
    ]

    for model in models:
        try:
            print(f"🔁 Trying model: {model}")
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            res.raise_for_status()
            data = res.json()
            if "choices" not in data:
                print("❌ OpenRouter missing 'choices' key.")
                continue

            content = data["choices"][0]["message"]["content"]
            return json.loads(content.strip())
        except Exception as e:
            print(f"❌ OpenRouter error: {e}")
            continue

    return []

# Use SerpAPI to search for images
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
        results = response.json()
        images = results.get("images_results", [])[:5]

        return [
            {
                "url": img.get("original") or img.get("thumbnail"),
                "desc": f"Image for query: {query}"
            }
            for img in images if img.get("original") or img.get("thumbnail")
        ]

    except Exception as e:
        print(f"❌ SerpAPI error for query '{query}':", e)
        return []

# Update domain_image_gems.json
def update_json_file(domain, subdomain, image_gems):
    try:
        with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    data.setdefault(domain, {}).setdefault(subdomain, {})["image_gems"] = image_gems

    with open(TAXONOMY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {domain} > {subdomain} successfully with {len(image_gems)} images.")
    print("👉 File saved at:", os.path.abspath(TAXONOMY_PATH))

def main():
    print(f"🔍 Enriching {DOMAIN} > {SUBDOMAIN} using OpenRouter + SerpAPI...")

    prompt = get_search_prompt(DOMAIN, SUBDOMAIN, LANGUAGE)
    keywords = fetch_keywords_from_openrouter(prompt)

    if not keywords:
        print("⚠️ No keywords returned from OpenRouter.")
        return

    all_images = []
    for kw in keywords:
        print(f"🔎 Searching for: {kw}")
        images = fetch_images_from_serpapi(kw)
        if images:
            all_images.extend(images)

    if all_images:
        update_json_file(DOMAIN, SUBDOMAIN, all_images)
    else:
        print("⚠️ No valid images found.")

if __name__ == "__main__":
    main()