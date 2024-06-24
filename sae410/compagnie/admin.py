from django.contrib import admin

from django.contrib import admin
from .models import Vol, Reservation, Achat
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

admin.site.register(Vol)
admin.site.register(Reservation)
admin.site.register(Achat)

