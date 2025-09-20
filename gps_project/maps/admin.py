from django.contrib import admin

from .models import TrafikSnapshot

@admin.register(TrafikSnapshot)
class TrafikSnapshotAdmin(admin.ModelAdmin):
    list_display = ('lokasi', 'masa', 'status', 'gambar')
    list_filter = ('lokasi', 'status')
    search_fields = ('lokasi',)

# Register your models here.
