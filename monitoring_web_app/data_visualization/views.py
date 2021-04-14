from django.shortcuts import render
from .models import Salle
from data_visualization.models import Climat_exterieur
from data_visualization.models import Montage
from data_visualization.models import Donnee_capteur
from data_visualization.models import Boitier

def data_visualization(request, montage_id):

    if montage_id == "meteo":
        salle = "meteo"
    else:
        salle = Salle.objects.get(
            boitier__montage__pk=montage_id)

    MontageActif = Montage.objects.filter(actif=True)
    salle_navbar = []
    donnees_navbar = []

    for x in MontageActif:  
        donnees_navbar.append(Donnee_capteur.objects.filter(montage = x.id).last())      
        salle_navbar.append(Salle.objects.filter(boitier__montage = x.id)[0])

    liste = list(zip(donnees_navbar, salle_navbar))

    context = {
        'dash_context': {'target_id': {'value': montage_id}},
        'salle': salle,
        'liste': liste,
        'enviroCanada':[Climat_exterieur.objects.last()]
    }
    return render(request, 'data_visualization/base.html', context)

def info(request, montage_id):

    MontageActif = Montage.objects.filter(actif=True)
    salle_navbar = []
    donnees_navbar = []

    for x in MontageActif:  
        donnees_navbar.append(Donnee_capteur.objects.filter(montage = x.id).last())      
        salle_navbar.append(Salle.objects.filter(boitier__montage = x.id)[0])

    liste = list(zip(donnees_navbar, salle_navbar))

    context = {
        'montage_id': montage_id,
        'boitier': Boitier.objects.filter(montage = montage_id)[0],
        'salle': Salle.objects.filter(boitier__montage = montage_id)[0],
        'montage': Montage.objects.filter(id = montage_id)[0],
        'liste': liste,
        'enviroCanada':[Climat_exterieur.objects.last()]
    }
    return render(request, 'data_visualization/info.html', context)