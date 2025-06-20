import os
import requests
import time
from bing_image_urls import bing_image_urls
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from duckduckgo_search import DDGS

# ================================
# Configuration
# ================================

categories ={
    "الطفولة_والرعاية": [
    "مراحل نمو الطفل بالصور", 
    "أنشطة تحفيزية للرضع", 
    "بطاقات نوم الطفل", 
    "رعاية الأمومة المصورة",
    "جداول تغذية الرضيع", 
    "صور رعاية حديثي الولادة", 
    "بيئة آمنة للأطفال", 
    "أنشطة تنمية المهارات الحركية"
]
,
"الاقتصاد_والمال": [
    "تصميمات تعليم الميزانية", 
    "رسم النقود والعملات العربية", 
    "رسم توضيحي للبنوك الإسلامية",
    "إنفوجرافيك التضخم والادخار", 
    "بطاقات سلوك المستهلك", 
    "رسوم توضيحية للتمويل الشخصي", 
    "مخططات الفقر والرفاه", 
    "صور الأسواق المالية العربية"
]
,
"الاختراعات_والتكنولوجيا": [
    "مخترعون عرب بالصور", 
    "ابتكارات تقنية عربية", 
    "صور أجهزة ذكية بالعربية", 
    "ملصقات أدوات كهربائية",
    "تصاميم أدوات ابتكارية", 
    "صور روبوتات مع تسميات", 
    "مخطط تطور التكنولوجيا", 
    "بطاقات أدوات إلكترونية"
]
,
"المهن_والوظائف": [
    "صور بيئة العمل", 
    "أدوات المهن المختلفة", 
    "رسم توضيحي لوظائف المستقبل",
    "بطاقات الحرف اليدوية", 
    "زي العمل حسب الوظيفة", 
    "رسم موظف في عمله", 
    "بطاقات الوظائف للأطفال", 
    "توضيح بيئات عمل متنوعة"
]
,
"الطعام_والعادات": [
    "عادات الأكل التقليدية", 
    "صور سفرة عربية", 
    "بطاقات آداب المائدة",
    "أطباق موسمية مصورة", 
    "ملصقات مكونات الوجبات", 
    "رسم أدوات المائدة", 
    "إنفوجرافيك هرم غذائي عربي", 
    "صور الطهي المنزلي"
]
,
"المناسبات_والاحتفالات": [
    "احتفالات النجاح الدراسية", 
    "صور يوم الطفل العربي", 
    "احتفالات بيئية مصورة",
    "بطاقات تهنئة عربية", 
    "ملصقات أعياد وطنية", 
    "صور تزيين الحفلات", 
    "ألعاب حفلات الأطفال", 
    "بطاقات يوم الأم والأب"
]
,
"الحيوانات_والطبيعة": [
    "حيوانات برية عربية", 
    "صور الطيور المحلية", 
    "ملصقات الحشرات الشائعة",
    "صور حيوانات المزرعة", 
    "بطاقات الحيوانات البحرية", 
    "تصنيف الحيوانات حسب البيئة", 
    "سلوك الحيوان بالصور", 
    "صور حيوانات الليل والنهار"
]
}

SAVE_ROOT = "arabic_images_4"
IMAGES_PER_SUBCATEGORY = 100
HEADERS = {'User-Agent': 'Mozilla/5.0'}
MAX_THREADS = 10

# ================================
# Scraper Functions
# ================================

def fetch_ddg_urls(query, max_results):
    urls = []
    try:
        with DDGS() as ddgs:
            for result in ddgs.images(query, max_results=max_results):
                image_url = result.get("image")
                if image_url:
                    urls.append(image_url)
    except Exception as e:
        print(f"[DuckDuckGo] Error for '{query}': {e}")
    return urls


def fetch_bing_urls(query, max_results):
    try:
        return bing_image_urls(query, limit=max_results)
    except Exception as e:
        print(f"[Bing] Failed for {query}: {e}")
        return []

def download_image(url, save_path):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content)).convert("RGB")
            image.save(save_path, "JPEG")
            return True
    except Exception:
        pass
    return False

def download_task(args):
    url, save_path = args
    return download_image(url, save_path)

# ================================
# Main Logic
# ================================

def scrape_and_save_images():
    os.makedirs(SAVE_ROOT, exist_ok=True)

    for category, subcategories in categories.items():
        category_path = os.path.join(SAVE_ROOT, category)
        os.makedirs(category_path, exist_ok=True)

        for subcat in subcategories:
            print(f"\n🔎 Scraping: {subcat} in category {category}")
            # query = subcat
            query = f"{subcat} صور تعليمية مكتوبة باللغة العربية بدون علامات مائية"
            urls = set()

            urls.update(fetch_ddg_urls(query, IMAGES_PER_SUBCATEGORY))
            urls.update(fetch_bing_urls(query, IMAGES_PER_SUBCATEGORY))

            print(f"🌐 Found {len(urls)} image URLs for {subcat}")

            download_tasks = []
            count = 0
            for url in urls:
                # if count >= IMAGES_PER_SUBCATEGORY:
                    # break
                filename = f"img_{subcat.replace(' ', '_')}_{str(count+1).zfill(4)}.jpg"
                save_path = os.path.join(category_path, filename)
                download_tasks.append((url, save_path))
                count += 1

            # Parallel Download
            print(f"⬇ Downloading {len(download_tasks)} images for {subcat} using {MAX_THREADS} threads...")
            success = 0
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                results = list(executor.map(download_task, download_tasks))

            success = sum(results)
            print(f"✅ Downloaded {success}/{len(download_tasks)} images for {subcat}")

# ================================
# Run Script
# ================================

if __name__ == "__main__":
    scrape_and_save_images()
