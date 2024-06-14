# sae410/compagnie/urls.py
from django.urls import path
from .views import (
    vol_list, vol_detail, reservation_detail, reservation_list, 
    achat_list, achat_detail, register, login, test_token
)

urlpatterns = [
    path('api/vols/', vol_list),
    path('api/vols/<int:pk>/', vol_detail),
    path('api/reservations/', reservation_list),
    path('api/reservations/<int:pk>/', reservation_detail),
    path('api/achats/', achat_list),
    path('api/achats/<int:pk>/', achat_detail),
    path('api/register/', register),
    path('api/login/', login),
    path('api/test_login/', test_token),
]