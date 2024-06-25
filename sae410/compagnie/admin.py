from django.contrib import admin

from django.contrib import admin
from .models import Vol, Reservation, Achat
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_nom', 'reservation_vol', 'delete_link')

    def delete_link(self, obj):
        return format_html('<a href="/rembourser/{}/">Annuler et rembourser</a>', obj.reservation_id)
    delete_link.short_description = 'Supprimer'

admin.site.register(Vol)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Achat)

