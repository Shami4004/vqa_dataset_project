import os
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO
from tqdm import tqdm

query = "brain MRI scan with annotations"
domain = "medicine"
subdomain = "radiology"
theme = "brain_scan"
language = "en"
num_images = 10

save_dir = f"../raw_images/{domain}/{subdomain}/{theme}"
os.makedirs(save_dir, exist_ok=True)

print(f"🔍 Searching: {query}")
results = []
with DDGS() as ddgs:
    for r in ddgs.images(query, max_results=num_images):
        results.append(r)

print(f"📥 Downloading {len(results)} images...")
count = 1
for result in tqdm(results):
    try:
        image_url = result["image"]
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))

        if image.width < 300 or image.height < 300:
            continue
        if image.width > 4 * image.height or image.height > 4 * image.width:
            continue

        file_path = os.path.join(save_dir, f"brain_scan_{count}.jpg")
        image.save(file_path)
        count += 1

    except Exception as e:
        print(f"Error: {e}")