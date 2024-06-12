from django.db import models
from django.contrib.auth.models import User

class Vol(models.Model):
    vol_id = models.AutoField(primary_key=True)
    vol_date_depart = models.DateTimeField()
    vol_date_arrive = models.DateTimeField()
    vol_lieu_depart = models.CharField(max_length=255)
    vol_lieu_arrive = models.CharField(max_length=255)
    vol_place_totale = models.IntegerField()
    vol_place_restante = models.IntegerField()
    vol_avion = models.CharField(max_length=255)
    vol_prix = models.IntegerField()

    def __str__(self):
        return f"Vol {self.vol_id} from {self.vol_lieu_depart} to {self.vol_lieu_arrive}"

class Achat(models.Model):
    achat_id = models.AutoField(primary_key=True)
    achat_iban = models.CharField(max_length=34)
    achat_date_prelevement = models.DateTimeField()
    achat_montant = models.FloatField()

    def __str__(self):
        return f"Achat {self.achat_id}"

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    reservation_nombre_personne = models.IntegerField()
    # reservation_nom = models.CharField(max_length=255)
    reservation_nom = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reservation_vol = models.ForeignKey(Vol, on_delete=models.CASCADE)
    reservation_date_creation = models.DateTimeField(auto_now_add=True)
    reservation_confirmation = models.ForeignKey(Achat, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Reservation {self.reservation_id} for {self.reservation_nom}"
