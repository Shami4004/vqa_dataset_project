import os, json
from PIL import Image

def generate_metadata_from_folder(domain, language):
    folder = f"../raw_images/{domain}_{language}"
    output_file = f"../metadata/{domain}_{language}.json"
    meta = []

    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            filepath = os.path.join(folder, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                meta.append({
                    "file_name": filename,
                    "width": width,
                    "height": height,
                    "language": language,
                    "domain": domain
                })
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_metadata_from_folder("urban", "ko")
    generate_metadata_from_folder("urban", "ja")
    generate_metadata_from_folder("urban", "ar")