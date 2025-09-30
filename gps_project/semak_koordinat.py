import cv2
import os

# 1. Gambar yang nak disemak
image_path = 'screenshots/images/trafik_Seremban_2025-09-26_11-45-31.png'

# 2. Semak kewujudan gambar
if not os.path.exists(image_path):
    print(f"[ERROR] Gambar '{image_path}' tak wujud.")
    exit()

# 3. Fungsi mouse untuk tunjuk koordinat
def show_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Koordinat: ({x}, {y})")

# 4. Baca dan papar gambar
image = cv2.imread(image_path)
cv2.imshow("Semak Koordinat", image)
cv2.setMouseCallback("Semak Koordinat", show_coordinates)
cv2.waitKey(0)
cv2.destroyAllWindows()