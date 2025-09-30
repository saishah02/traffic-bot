from django.urls import path
from . import views

urlpatterns = [
    path('', views.trafik_view, name='trafik'),
    path('trafik/', views.trafik_view, name='trafik_view'),
    path('latest-image/', views.trafik_view, name='latest_image'),
        path('senarai/', views.senarai_trafik, name='senarai_trafik'),
    path('satellite/', views.satellite_view, name='satellite_view'),
    
]