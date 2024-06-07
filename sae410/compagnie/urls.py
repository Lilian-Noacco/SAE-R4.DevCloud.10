from django.urls import path
from .views import vol_list, vol_detail

urlpatterns = [
    path('api/', vol_list),
    path ('api/vol/<int:id>/', vol_detail),
]