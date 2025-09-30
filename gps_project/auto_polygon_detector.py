import cv2
import numpy as np
import os

# 1. Folder input/output
image_folder = 'screenshots/images'
output_folder = 'screenshots/hasil_rectangle'
os.makedirs(output_folder, exist_ok=True)

# 2. Warna kesesakan dalam HSV
color_ranges = {
    "Hijau":   ([35, 50, 50], [85, 255, 255]),
    "Kuning": ([25, 50, 50], [35, 255, 255]),
    "Oren":   ([10, 50, 50], [25, 255, 255]),
    "Merah":  ([0, 50, 50],  [10, 255, 255]),
    "Maroon": ([0, 50, 20],  [5, 255, 80])
}

# 3. Senarai gambar
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_files.sort()

# 4. Proses setiap gambar
for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"[SKIP] Gagal baca '{filename}'")
        continue

    print(f"\n📌 Proses: {filename}")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    found = False

    # 5. Loop setiap warna kesesakan
    for label, (lower, upper) in color_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        mask = cv2.inRange(hsv, lower_np, upper_np)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                found = True
                print(f"  ✔ Rectangle atas warna {label}")
                break
        if found:
            break

    if not found:
        print("  ✘ Tiada kawasan warna kesesakan yang sesuai.")

    # 6. Simpan hasil
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, image)
    print(f"  ➤ Disimpan ke: {output_path}")