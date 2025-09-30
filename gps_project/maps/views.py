from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

def get_latest_image_info(mode=None):
    folder = os.path.join(settings.BASE_DIR, 'maps', 'static', 'images')
    latest_image = None
    files_info = []

    if os.path.exists(folder):
        images = sorted(
            [img for img in os.listdir(folder)
             if img.lower().endswith('.png') and (mode is None or img.startswith(mode + "_"))],
            key=lambda x: os.path.getmtime(os.path.join(folder, x)),
            reverse=True
        )

        for img in images:
            file_path = os.path.join(folder, img)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            size = os.stat(file_path).st_size
            file_info = {
                'name': img,
                'modified': modified,
                'size': size,
                'type': 'PNG',
                'filename': f"images/{img}"
            }
            files_info.append(file_info)

        if images:
            img = images[0]
            parts = img.replace('.png', '').split('_')

            if len(parts) >= 4:
                extracted_mode = parts[0]
                lokasi = parts[1]
                date_str = parts[2]
                time_str = parts[3]

                try:
                    masa_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H-%M-%S")
                    masa = masa_obj.strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    logger.warning(f"Invalid date format in filename: {img} → {e}")
                    masa = f"{date_str} {time_str}"

                latest_image = {
                    'filename': f"images/{img}",
                    'lokasi': lokasi,
                    'masa': masa,
                    'mode': extracted_mode
                }
            else:
                latest_image = {
                    'filename': f"images/{img}",
                    'lokasi': "Tidak diketahui",
                    'masa': "Format masa tidak sah",
                    'mode': mode or "tidak_dikenalpasti"
                }

    if not latest_image:
        latest_image = {
            'filename': 'images/gambar_default.png',
            'lokasi': 'Fallback',
            'masa': 'Tidak tersedia',
            'mode': mode or 'default'
        }

    return latest_image, files_info

def satellite_view(request):
    latest_image, _ = get_latest_image_info(mode='satelit')
    return render(request, 'satellite.html', {'latest_image': latest_image})

def trafik_view(request):
    latest_image, files_info = get_latest_image_info(mode='trafik')

 
    return render(request, 'trafik.html', {
        'latest_image': latest_image,
        'files_info': files_info
    })

def senarai_trafik(request):
    try:
        snapshots = TrafikSnapshot.objects.order_by('-masa')[:50]
    except Exception as e:
        logger.error(f"Error fetching snapshots: {e}")
        snapshots = []

    return render(request, 'senarai.html', {'snapshots': snapshots})