from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import TrafikSnapshot
import os
import logging

logger = logging.getLogger(__name__)

def trafik_view(request):
    folder = os.path.join(settings.BASE_DIR, 'screenshots', 'images')
    latest_image = None

    if os.path.exists(folder):
        # Cari semua fail .png dan susun ikut masa fail (terbalik = terbaru dulu)
        images = sorted(
            [img for img in os.listdir(folder) if img.lower().endswith('.png')],
            key=lambda x: os.path.getmtime(os.path.join(folder, x)),
            reverse=True
        )

        if images:
            img = images[0]
            parts = img.replace('.png', '').split('_')

            if len(parts) >= 4:
                mode = parts[0]
                lokasi = parts[1]
                masa = parts[2] + ' ' + parts[3].replace('-', ':')
            else:
                mode = "Tidak diketahui"
                lokasi = "Tidak diketahui"
                masa = "Format masa tidak sah"

            latest_image = {
                'filename': os.path.join('images', img),  # relative path for MEDIA_URL
                'mode': mode,
                'lokasi': lokasi,
                'masa': masa
            }

    return render(request, 'trafik.html', {
        'latest_image': latest_image,
        'MEDIA_URL': settings.MEDIA_URL
    })



def latest_image(request):
    folder = os.path.join(settings.BASE_DIR, 'screenshots', 'images')
    latest_image = None

    if os.path.exists(folder):
        images = sorted(
            [img for img in os.listdir(folder) if img.endswith('.png')],
            key=lambda x: os.path.getmtime(os.path.join(folder, x)),
            reverse=True
        )

        for img in images:
            parts = img.replace('.png', '').split('_')
            if len(parts) == 2:
                snapshot_id, mode = parts
                try:
                    snapshot = TrafikSnapshot.objects.get(id=snapshot_id)
                    latest_image = {
                        'id': snapshot.id,
                        'lokasi': snapshot.lokasi,
                        'masa': snapshot.masa.strftime('%Y-%m-%d %H:%M:%S'),
                        'filename_trafik': f"{mode}_{lokasi}_{timestamp}_trafik.png",
                        'filename_satelit': f"{mode}_{lokasi}_{timestamp}_satelit.png"
                    }
                    break
                except TrafikSnapshot.DoesNotExist:
                    logger.warning(f"TrafikSnapshot with ID {mode}_{lokasi}_{timestamp} not found.")
                    continue

    return JsonResponse({'latest_image': latest_image})


def senarai_trafik(request):
    try:
        snapshots = TrafikSnapshot.objects.order_by('-masa')[:50]
    except Exception as e:
        logger.error(f"Error fetching snapshots: {e}")
        snapshots = []

    return render(request, 'senarai.html', {'snapshots': snapshots})