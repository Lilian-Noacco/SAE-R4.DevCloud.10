from django.contrib import admin

from django.contrib import admin
from .models import Vol, Reservation, Achat

admin.site.register(Vol)
admin.site.register(Reservation)
admin.site.register(Achat)