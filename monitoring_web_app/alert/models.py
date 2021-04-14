from django.db import models

# Create your models here.


class Responsable(models.Model):
    prenom = models.CharField(max_length=30)
    nom = models.CharField(max_length=30)
    email = models.CharField(max_length=75)

    def __str__(self):
        return self.prenom + " " + self.nom
