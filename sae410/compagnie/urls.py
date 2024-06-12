from django.urls import path
from .views import vol_list, vol_detail, reservation_detail, reservation_list, achat_list, achat_detail

urlpatterns = [
    path('api/', vol_list),
    path ('api/vol/<int:id>/', vol_detail),
    path ('api/reservation/', reservation_list),
    path ('api/reservation/<int:id>/', reservation_detail),
]