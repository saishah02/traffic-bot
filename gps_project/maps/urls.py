from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.peta_view, name='peta'),
    path('', views.trafik_view, name='trafik'),
    path('latest-image/', views.latest_image_json, name='latest_image_json'),
]