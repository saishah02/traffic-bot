from django.db import models
from uuid import uuid4
import os

def generate_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{instance.mode}.{ext}"
    return os.path.join('images', filename)

class TrafikSnapshot(models.Model):
    STATUS_CHOICES = [
        ('Lancar', 'Lancar'),
        ('Sesak', 'Sesak'),
        ('Kemalangan', 'Kemalangan'),
    ]

    MODE_CHOICES = [
        ('trafik', 'Traffic View'),
        ('satelit', 'Satellite View'),
        ('standard', 'Standard Map'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    lokasi = models.CharField(max_length=100)
    masa = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    gambar = models.ImageField(upload_to='images/')  # stored in MEDIA_ROOT/images/
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='trafik')

    def __str__(self):
        lokasi_display = self.lokasi if self.lokasi else "Lokasi tidak diketahui"
        masa_display = self.masa.strftime('%Y-%m-%d %H:%M') if self.masa else "(no timestamp)"
        return f"{lokasi_display} - {masa_display}"

    class Meta:
        verbose_name = "Traffic Snapshot"
        verbose_name_plural = "Traffic Snapshots"
        ordering = ['-masa']