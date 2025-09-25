from django.urls import path
from . import views

urlpatterns = [
    path('', views.trafik_view, name='trafik'),
    path('latest-image/', views.latest_image, name='latest_image_json'),
]