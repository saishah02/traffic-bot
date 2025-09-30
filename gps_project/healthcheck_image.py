import os
from PIL import Image

FOLDER = os.path.join(os.getcwd(), 'screenshots', 'images')

def check_image(file):
    path = os.path.join(FOLDER, file)
    try:
        with Image.open(path) as img:
            img.verify()  # Check if image is readable
        return True
    except Exception as e:
        return False

def is_valid_format(file):
    parts = file.replace('.png', '').split('_')
    return len(parts) >= 4 and parts[0] in ['trafik', 'satelit']

def run_healthcheck():
    if not os.path.exists(FOLDER):
        print("❌ Folder not found:", FOLDER)
        return

    files = [f for f in os.listdir(FOLDER) if f.lower().endswith('.png')]
    if not files:
        print("⚠️ No PNG files found.")
        return

    print(f"🔍 Checking {len(files)} image(s)...\n")

    for f in sorted(files):
        readable = check_image(f)
        format_ok = is_valid_format(f)

        status = []
        if readable:
            status.append("✅ readable")
        else:
            status.append("❌ unreadable")

        if format_ok:
            status.append("🆗 format")
        else:
            status.append("📛 bad format")

        print(f"{f}: {' | '.join(status)}")

if __name__ == "__main__":
    run_healthcheck()