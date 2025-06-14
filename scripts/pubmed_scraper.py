import os
import requests
from tqdm import tqdm
from xml.etree import ElementTree as ET
from Bio import Entrez

# ---- Config ----
Entrez.email = "your_email@example.com"  # Replace with your actual email
query = "annotated brain MRI"
max_articles = 15
save_dir = "../raw_images/medicine/radiology/brain_scan"
os.makedirs(save_dir, exist_ok=True)

print("🔍 Searching PubMed Central...")
handle = Entrez.esearch(db="pmc", term=query, retmax=max_articles)
record = Entrez.read(handle)
pmc_ids = record["IdList"]

print(f"✅ Found {len(pmc_ids)} articles")

valid_extensions = [".jpg", ".jpeg", ".png"]
count = 1

for pmc_id in tqdm(pmc_ids):
    try:
        fetch = Entrez.efetch(db="pmc", id=pmc_id, rettype="full", retmode="xml")
        tree = ET.parse(fetch)
        root = tree.getroot()

        for fig in root.findall(".//fig"):
            graphic = fig.find(".//graphic")
            if graphic is not None:
                href = graphic.attrib.get("{http://www.w3.org/1999/xlink}href")
                if href:
                    # Only download image if it ends with a known image extension
                    if not any(href.lower().endswith(ext) for ext in valid_extensions):
                        continue

                    image_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/bin/{href}"
                    try:
                        response = requests.get(image_url, timeout=10)
                        if response.status_code == 200 and response.content:
                            file_path = os.path.join(save_dir, f"brain_scan_{count}.jpg")
                            with open(file_path, "wb") as f:
                                f.write(response.content)
                            count += 1
                    except Exception as err:
                        print(f"⚠️ Failed to download {image_url}: {err}")
    except Exception as e:
        print(f"⛔ Error with article {pmc_id}: {e}")