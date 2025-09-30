import cv2
import numpy as np
import os

# 1. Folder input dan output
image_folder = 'screenshots/images'
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# 2. Semak kewujudan folder input
if not os.path.exists(image_folder):
    print(f"[ERROR] Folder '{image_folder}' tak wujud.")
    exit()

# 3. Fungsi klasifikasi kesesakan
def classify_congestion(hue_values):
    if len(hue_values) == 0:
        return "Tiada pixel dalam polygon"
    
    avg_hue = np.mean(hue_values)
    print("  ↪ Purata hue:", avg_hue)

    if 35 < avg_hue < 85:
        return "Hijau - Tidak sesak"
    elif 25 < avg_hue <= 35:
        return "Kuning - Kurang sesak"
    elif 10 < avg_hue <= 25:
        return "Oren - Sedikit sesak"
    elif 0 < avg_hue <= 10:
        return "Merah - Sangat sesak"
    elif avg_hue <= 5:
        return "Maroon - Sangat sangat sesak"
    else:
        return "Tidak pasti"

# 4. Senarai gambar
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_files.sort()

if not image_files:
    print("[ERROR] Tiada gambar dalam folder.")
    exit()

# 5. Proses setiap gambar
for filename in image_files:
    image_path = os.path.join(image_folder, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"[SKIP] Gagal baca '{filename}' — mungkin format tak support atau fail rosak.")
        continue

    # 6. Rectangle panjang (20% width, 8% height)
    height, width = image.shape[:2]
    rect_w, rect_h = int(width * 0.20), int(height * 0.08)
    center_x, center_y = width // 2, height // 2

    # Asal rectangle (sebelum rotate)
    rect = np.array([
        [center_x - rect_w // 2, center_y - rect_h // 2],
        [center_x + rect_w // 2, center_y - rect_h // 2],
        [center_x + rect_w // 2, center_y + rect_h // 2],
        [center_x - rect_w // 2, center_y + rect_h // 2]
    ], dtype=np.float32)

    # 7. Rotate 35° ke kiri
    angle = -35
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
    rotated_rect = cv2.transform(np.array([rect]), M)[0]

    # 8. Gerakkan ke kiri dan ke atas
    shift_x = -70  # ke kiri
    shift_y = -60  # ke atas
    rotated_rect[:, 0] += shift_x
    rotated_rect[:, 1] += shift_y

    polygon_coords = rotated_rect.astype(np.int32)

    # 9. Buat mask dan extract pixel
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [polygon_coords], 255)
    masked_pixels = cv2.bitwise_and(image, image, mask=mask)

    # 10. Convert ke HSV dan ambil hue
    hsv = cv2.cvtColor(masked_pixels, cv2.COLOR_BGR2HSV)
    hue_values = hsv[:, :, 0][mask == 255]

    # 11. Klasifikasi
    print(f"[INFO] {filename}")
    status = classify_congestion(hue_values)

    # 12. Lukis polygon dan status
    cv2.polylines(image, [polygon_coords], isClosed=True, color=(0,255,0), thickness=2)
    text_x, text_y = polygon_coords[0][0], polygon_coords[0][1] - 10
    cv2.putText(image, status, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # 13. Simpan imej dan status
    output_image_path = os.path.join(output_folder, f"result_{filename}")
    output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_status.txt")

    cv2.imwrite(output_image_path, image)
    with open(output_text_path, 'w') as f:
        f.write(status)

    print(f"  ↪ Disimpan: {output_image_path}")
    print(f"  ↪ Status: {status}")