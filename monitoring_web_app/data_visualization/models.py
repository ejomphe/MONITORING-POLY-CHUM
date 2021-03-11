from django.db import models
from django.utils import timezone

# Create your models here.


# Admin
class Salle(models.Model):
    nom_salle = models.CharField(max_length=20)
    departement = models.CharField(max_length=30)
    numero_equipement = models.CharField(max_length=10)
    ahu = models.CharField(max_length=10)
    seuil_temp_min_c = models.DecimalField(max_digits=5, decimal_places=2)
    seuil_temp_max_c = models.DecimalField(max_digits=5, decimal_places=2)
    seuil_hum_min_rh = models.DecimalField(max_digits=5, decimal_places=2)
    seuil_hum_max_rh = models.DecimalField(max_digits=5, decimal_places=2)
    seuil_press_min_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    seuil_press_max_kpa = models.DecimalField(max_digits=5, decimal_places=2)

class Boitier(models.Model):                               # Admin
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    # On parle ici de la description du l'endroit ou on a placé le boitier ex. coin nord-ouest
    emplacement = models.CharField(max_length=30)
    ahu = models.CharField(max_length=10)
    date_fabrication = models.DateField()
    materiel = models.CharField(max_length=20)
    numero_imprimante_fabrication = models.CharField(max_length=20)
    nom_fichier_cad = models.CharField(max_length=50)


# Admin   (note un montage = capteur + micro)
class Montage(models.Model):
    boitier = models.ForeignKey(Boitier, on_delete=models.CASCADE)
    modele_capteur = models.CharField(max_length=10)
    modele_microcontroleur = models.CharField(max_length=10)
    offset_temp = models.DecimalField(max_digits=5, decimal_places=3)
    ord_orig_temp = models.DecimalField(max_digits=5, decimal_places=3)
    offset_hum = models.DecimalField(max_digits=5, decimal_places=3)
    ord_orig_hum = models.DecimalField(max_digits=5, decimal_places=3)
    offset_pres = models.DecimalField(max_digits=5, decimal_places=3)
    ord_orig_pres = models.DecimalField(max_digits=5, decimal_places=3)
    date_derniere_calibration = models.DateField()
    date_prochaine_calibration = models.DateField()
    actif = models.BooleanField()

    def __str__(self):
        return str(self.pk)


# environnement canada (web crawler)
class Climat_exterieur(models.Model):
    timestamp = models.DateTimeField()
    temp_c = models.DecimalField(max_digits=5, decimal_places=2)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    donnee_aberrante = models.BooleanField()
    timestamp_sys1 = models.DateTimeField(default=timezone.now)
    timestamp_sys2 = models.DateTimeField(auto_now=True)


# Panne environnement canada   # Surement à retirer éventuellement.
class Erreur_climat_exterieur(models.Model):
    timestamp = models.DateTimeField()
    temp_c = models.DecimalField(max_digits=5, decimal_places=2)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp_sys = models.DateTimeField(auto_now_add=True)


class Donnee_capteur(models.Model):
    montage = models.ForeignKey(Montage, on_delete=models.CASCADE)
    temp_c = models.DecimalField(max_digits=5, decimal_places=2)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    donnee_aberrante = models.BooleanField()
    donnee_de_panne = models.BooleanField()
    # retire éventuellement quand RTC fonctionne.
    timestamp_sys = models.DateTimeField(auto_now_add=True)
    real_time_clock = models.DateTimeField()


class Donnee_aberrante_capteur(models.Model):
    montage = models.ForeignKey(Montage, on_delete=models.CASCADE)
    temp_c = models.DecimalField(max_digits=5, decimal_places=2)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    # retire éventuellement quand RTC fonctionne.
    timestamp_sys = models.DateTimeField(auto_now_add=True)
    real_time_clock = models.DateTimeField()


# quand envoie lecture carte SD.
class Panne_de_service(models.Model):
    montage = models.ForeignKey(Montage, on_delete=models.CASCADE)
    temp_c = models.DecimalField(max_digits=5, decimal_places=2)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2)
    # retire éventuellement quand RTC fonctionne.
    timestamp_sys = models.DateTimeField(auto_now_add=True)
    real_time_clock = models.DateTimeField()
