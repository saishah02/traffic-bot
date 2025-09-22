import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Force UTF-8 encoding to avoid UnicodeEncodeError
sys.stdout.reconfigure(encoding='utf-8')

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gps_project.settings')

import django
django.setup()

from django.utils import timezone
from maps.models import TrafikSnapshot

# Output folder
output_folder = os.path.join(BASE_DIR, "screenshots", "images")
os.makedirs(output_folder, exist_ok=True)

# Setup Chrome options
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

# Initialize Chrome driver
try:
    driver = webdriver.Chrome(options=options)
except Exception as driver_error:
    print(f"❌ Failed to start ChromeDriver: {driver_error}")
    sys.exit(1)

lokasi = "Seremban"

# Define URLs for each mode
URLS = {
    "trafik": "https://www.google.com/maps/@2.7258,101.9424,13z/data=!5m1!1e1",         # Traffic mode
    "satelit": "https://www.google.com/maps/@2.7258,101.9424,13z/data=!3m1!1e3",        # Satellite mode
}

print("🚦 Screenshot bot started...")

MODES = ["trafik", "satelit"]  # You can add more modes later

while True:
    for mode in MODES:
        try:
            url = URLS[mode]
            driver.get(url)
            time.sleep(5)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{mode}_{lokasi}_{timestamp}.png"
            filepath = os.path.join(output_folder, filename)

            driver.save_screenshot(filepath)
            print(f"✅ Screenshot ({mode}) disimpan: {filepath}")

            # Save metadata to DB
            try:
                TrafikSnapshot.objects.create(
                    lokasi=lokasi,
                    masa=timezone.now(),
                    status='Sesak',  # You can automate this later
                    gambar=os.path.join("images", filename),
                    mode=mode  # Add this field to your model
                )
                print(f"🗂️ Metadata ({mode}) saved to DB.")
            except Exception as db_error:
                print(f"❌ DB error ({mode}): {db_error}")

            time.sleep(5)  # Short pause between modes

        except Exception as e:
            print(f"❌ Screenshot error ({mode}): {e}")
            time.sleep(60)

    time.sleep(300)  # Wait 5 minutes before next full cycle
