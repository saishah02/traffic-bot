import os
import sys
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3
import cv2
import numpy as np

def safe_print(msg, emoji=""):
    try:
        print(f"{emoji} {msg}")
    except UnicodeEncodeError:
        print(msg)

# Setup DB
db_path = os.path.abspath("db.sqlite3")
safe_print("Bot is using DB path: " + db_path, "📁")
conn = sqlite3.connect(db_path)

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gps_project.settings')

import django
django.setup()

from django.utils import timezone
from maps.models import TrafikSnapshot

# Folder setup
screenshot_folder = os.path.join(BASE_DIR, "screenshots", "images")
static_folder = os.path.join(BASE_DIR, "maps", "static", "images")
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(static_folder, exist_ok=True)

# Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-sync")
options.add_argument("--disable-extensions")
options.add_argument("--disable-component-update")
options.add_argument("--disable-notifications")
options.add_argument("--mute-audio")
options.add_argument("--disable-cloud-import")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Start Chrome
try:
    driver = webdriver.Chrome(options=options)
except Exception as driver_error:
    safe_print(f"Failed to start ChromeDriver: {driver_error}", "❌")
    sys.exit(1)

lokasi = "PasirGudang"

URLS = {
    "trafik": "https://www.google.com/maps/@1.4827462,103.9046154,13z/data=!5m1!1e1",
    "satelit": "https://www.google.com/maps/@1.4827965,103.9046793,123m/data=!3m1!1e3!5m1!1e1?entry=ttu&g_ep=EgoyMDI1MDkyNC4wIKXMDSoASAFQAw%3D%3D",
}

safe_print("Screenshot bot started...", "🚦")

MODES = ["trafik", "satelit"]

while True:
    for mode in MODES:
        try:
            url = URLS[mode]
            driver.get(url)
            time.sleep(5)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{mode}_{lokasi}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_folder, filename)
            static_path = os.path.join(static_folder, filename)

            # Save screenshot
            driver.save_screenshot(screenshot_path)
            safe_print(f"Screenshot ({mode}) saved: {screenshot_path}", "✅")

            # Copy to static/images
            try:
                shutil.copy(screenshot_path, static_path)
                safe_print(f"Copied to static/images: {static_path}", "📂")
            except Exception as copy_error:
                safe_print(f"Failed to copy to static/images: {copy_error}", "❌")

            # Save metadata to DB
            try:
                TrafikSnapshot.objects.create(
                    lokasi=lokasi,
                    masa=timezone.now(),
                    status='Sesak',
                    gambar=os.path.join("images", filename),  # ✅ relative to static/
                    mode=mode
                )
                safe_print(f"Metadata ({mode}) saved to DB.", "🗂️")
            except Exception as db_error:
                safe_print(f"DB error ({mode}): {db_error}", "❌")

            time.sleep(5)

        except Exception as e:
            safe_print(f"Screenshot error ({mode}): {e}", "❌")
            time.sleep(60)

    time.sleep(300)