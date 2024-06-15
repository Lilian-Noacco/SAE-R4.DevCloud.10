from django.urls import path
from .views import vol_list, vol_detail, reservation_detail, reservation_list, achat_list, achat_detail, register, login, test_token

urlpatterns = [
    path('api/', vol_list),
    path ('api/vol/<int:pk>/', vol_detail),
    path ('api/reservation/', reservation_list),
    path ('api/reservation/<int:pk>/', reservation_detail),
    path ('api/achat/', achat_list),
    path ('api/achat/<int:pk>/', achat_detail),
    path ('api/register/', register),
    path ('api/login/', login),
    path ('api/test_login/', test_token),
]
