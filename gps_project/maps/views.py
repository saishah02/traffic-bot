from django.shortcuts import render
from django.conf import settings
import os
from django.http import JsonResponse
from .models import TrafikSnapshot

def peta_view(request):
    return render(request, 'peta.html')

def trafik_view(request):
    folder = os.path.join(settings.BASE_DIR, 'screenshots', 'images')
    latest_image = None

    if os.path.exists(folder):
        # Ambil semua fail .png dan susun ikut masa (terbalik = terbaru dulu)
        images = sorted(
            [img for img in os.listdir(folder) if img.lower().endswith('.png')],
            reverse=True
        )

        if images:
            img = images[0]  # ambil fail paling baru
            parts = img.replace('.png', '').split('_')

            # Cuba extract lokasi dan masa, fallback kalau format pelik
            if len(parts) >= 4:
                lokasi = parts[1]
                masa = parts[2] + ' ' + parts[3].replace('-', ':')
            else:
                lokasi = "Tidak diketahui"
                masa = "Format masa tidak sah"

            latest_image = {
                'filename': os.path.join('images', img),  # relative to MEDIA_URL
                'lokasi': lokasi,
                'masa': masa
            }

    return render(request, 'trafik.html', {
        'latest_image': latest_image,
        'MEDIA_URL': settings.MEDIA_URL
    })

def latest_image_json(request):
    folder = os.path.join(settings.BASE_DIR, 'screenshots', 'images')
    latest_image = None

    if os.path.exists(folder):
        # Ambil semua fail .png dan susun ikut masa fail (terbalik = terbaru dulu)
        images = sorted(
            [img for img in os.listdir(folder) if img.endswith('.png')],
            key=lambda x: os.path.getmtime(os.path.join(folder, x)),
            reverse=True
        )

        # Cari fail pertama yang sah (ada format {uuid}_{mode}.png)
        for img in images:
            parts = img.replace('.png', '').split('_')
            if len(parts) == 2:
                snapshot_id, mode = parts
                try:
                    snapshot = TrafikSnapshot.objects.get(id=snapshot_id)
                    latest_image = {
                        'id': snapshot_id,
                        'lokasi': snapshot.lokasi,
                        'masa': snapshot.masa.strftime('%Y-%m-%d %H:%M:%S'),
           "filename_trafik": f"{snapshot.id}_trafik.png",
            "filename_satelit": f"{snapshot.id}_satelit.png"

                    }
                    break  # stop after first valid match
                except TrafikSnapshot.DoesNotExist:
                    continue  # try next image

    return JsonResponse({'latest_image': latest_image})
   
def senarai_trafik(request):
    snapshots = TrafikSnapshot.objects.order_by('-masa')[:50]
    return render(request, 'senarai.html', {'snapshots': snapshots})
