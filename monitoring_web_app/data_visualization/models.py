from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


# Admin
class Salle(models.Model):
    nom_salle = models.CharField(max_length=20, verbose_name="Nom de salle")
    departement = models.CharField(max_length=30, verbose_name="Département")
    numero_equipement = models.CharField(
        max_length=10, blank=True, verbose_name="Numéro d'équipement")
    ahu = models.CharField(max_length=10, blank=True,
                           verbose_name="Air handling unit")
    seuil_temp_min_c = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil température minimale", help_text="Ces seuils serviront à l'envoie d'alertes et seront affichés dans les graphiques de visualisation de données")
    seuil_temp_max_c = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil température maximale")
    seuil_hum_min_rh = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil humidité minimale")
    seuil_hum_max_rh = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil humidité maximale")
    seuil_press_min_kpa = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil pression minimale")
    seuil_press_max_kpa = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Seuil pression maximale")

    def __str__(self):
        return self.nom_salle


"""
Optimisation BD

# class Parametre_environnement(models.Models):
# 	parametre = models.CharField(max_length=30)


# class Parametre_calibration(models.Models):
# 	parametre = models.CharField(max_length=30)


# class Min_max(models.Models):
# 	parametre = models.CharField(max_length=30)


# class Salle_seuil(models.Models):
# 	salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
#     parameter_environnement = models.ForeignKey(Parametre_environnement, on_delete=models.CASCADE)
# 	min_max= models.ForeignKey(Min_max, on_delete=models.CASCADE)
# 	valeur= models.DecimalField(max_digits=5, decimal_places=2)

# class Montage_calibration(models.Models):
# 	montage = models.ForeignKey(montage, on_delete=models.CASCADE)
#     parameter_environnement = models.ForeignKey(Parametre_environnement, on_delete=models.CASCADE)
# 	parameter_calibration= models.ForeignKey(Parametre_calibration, on_delete=models.CASCADE)
# 	valeur= models.DecimalField(max_digits=5, decimal_places=3)

"""


class Boitier(models.Model):                               # Admin
    nom_boitier = models.CharField(
        max_length=20, verbose_name="Nom du boîtier", default="")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    # On parle ici de la description du l'endroit ou on a placé le boitier ex. coin nord-ouest
    emplacement = models.CharField(max_length=30, blank=True, )
    date_fabrication = models.DateField(
        blank=True, null=True, verbose_name="Date de fabrication")
    materiel = models.CharField(
        max_length=20, blank=True, verbose_name="Matériel")
    numero_imprimante_fabrication = models.CharField(
        max_length=20, blank=True, verbose_name="Numéro d'imprimante de fabrication")
    nom_fichier_cad = models.CharField(
        max_length=50, blank=True, verbose_name="Nom du fichier CAD")

    def __str__(self):
        return self.nom_boitier

# Admin   (note un montage = capteur + micro)


class Montage(models.Model):
    nom_montage = models.CharField(
        max_length=20, verbose_name="Nom du montage", default="")
    boitier = models.ForeignKey(Boitier, on_delete=models.CASCADE)
    modele_capteur = models.CharField(
        max_length=10, blank=True, verbose_name="Modèle capteur")
    modele_microcontroleur = models.CharField(
        max_length=10, blank=True, verbose_name="Modèle microcontrôleur")
    offset_temp = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Offset température", help_text="Les champs \"Offset\" et \"Ordonnée à l'origine\" sont obtenus lors de l'étalonnage")
    ord_orig_temp = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Ordonnee à l'origine température")
    offset_hum = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Offset humidité")
    ord_orig_hum = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Ordonnee à l'origine humidité")
    offset_pres = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Offset pression")
    ord_orig_pres = models.DecimalField(
        max_digits=5, decimal_places=3, verbose_name="Ordonnee à l'origine pression")
    date_derniere_calibration = models.DateField(
        blank=True, null=True, verbose_name="Date de la dernière calibration")
    date_prochaine_calibration = models.DateField(
        blank=True, null=True, verbose_name="Date de la prochaine calibration")
    responsable = models.ManyToManyField('alert.Responsable')
    actif = models.BooleanField(
        help_text="Cette option doit être sélectionnée pour afficher les données de ce montage sur le site")

    def __str__(self):
        return self.nom_montage


# environnement canada (web crawler)
class Climat_exterieur(models.Model):
    timestamp = models.DateTimeField()
    temp_c = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    donnee_aberrante = models.BooleanField(null=True)


class Donnee_capteur(models.Model):
    montage = models.ForeignKey(Montage, on_delete=models.CASCADE)
    temp_c = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    hum_rh = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pres_kpa = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    donnee_aberrante = models.BooleanField()
    donnee_de_panne = models.BooleanField()
    donnee_moyennee = models.BooleanField()
    real_time_clock = models.DateTimeField(null=True)
