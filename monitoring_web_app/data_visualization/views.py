from django.shortcuts import render
from .models import Salle
from data_visualization.models import Climat_exterieur
from data_visualization.models import Montage
from data_visualization.models import Donnee_capteur
from data_visualization.models import Boitier


def data_visualization(request, nom_montage):

    if nom_montage == "meteo":
        salle = "meteo"
        montage_id = "meteo"
    else:
        salle = Salle.objects.get(
            boitier__montage__nom_montage=nom_montage)
        montage_id = Montage.objects.get(nom_montage=nom_montage).pk

    MontageActif = Montage.objects.filter(actif=True)
    salle_navbar = []
    donnees_navbar = []

    for x in MontageActif:
        donnees_navbar.append(
            Donnee_capteur.objects.filter(montage=x.id).last())
        salle_navbar.append(Salle.objects.get(boitier__montage=x.id))

    liste = list(zip(donnees_navbar, salle_navbar))

    context = {
        'dash_context': {'target_id': {'value': montage_id}},
        'nom_montage': nom_montage,
        'salle': salle,
        'liste': liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }
    return render(request, 'data_visualization/base.html', context)


def info(request, nom_montage):

    montage_id = Montage.objects.get(nom_montage=nom_montage).pk
    MontageActif = Montage.objects.filter(actif=True)
    salle_navbar = []
    donnees_navbar = []

    for x in MontageActif:
        donnees_navbar.append(
            Donnee_capteur.objects.filter(montage=x.id).last())
        salle_navbar.append(Salle.objects.get(boitier__montage=x.id))

    liste = list(zip(donnees_navbar, salle_navbar))

    context = {
        'nom_montage': nom_montage,
        'montage_id': montage_id,
        'boitier': Boitier.objects.get(montage=montage_id),
        'salle': Salle.objects.get(boitier__montage=montage_id),
        'montage': Montage.objects.get(id=montage_id),
        'liste': liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }
    return render(request, 'data_visualization/info.html', context)
