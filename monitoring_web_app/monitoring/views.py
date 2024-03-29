from django.shortcuts import render
from data_visualization.models import Donnee_capteur, Salle, Montage, Boitier, Climat_exterieur


def listeDepartement(departements):

    departementsUnique = []
    departementsUnique = list(dict.fromkeys(departements))

    return departementsUnique


def home(request):

    MontageActif = (Montage.objects.filter(actif=True))
    salles = []
    departements = []
    donnees = []
    noms_montage = []
    for x in MontageActif:
        derniere_donnee = Donnee_capteur.objects.filter(
            montage=x.id, donnee_aberrante=False).last()

        '''
        Cette condition permet d'éviter que le site plante quand on ajoute un nouveau dispositif
        qu'il est actif, mais qu'il n'a pas encore enregistré une donnée.
        '''
        if derniere_donnee != None:
            donnees.append(derniere_donnee)
            salle = Salle.objects.get(boitier__montage__pk=x.id)
            salles.append(salle)
            departements.append(Salle.objects.get(
                boitier__montage__pk=x.id).departement)
            noms_montage.append(x.nom_montage)

    liste = list(zip(donnees, salles, noms_montage))

    context = {
        'salle_navbar': salles,
        'departements': listeDepartement(departements),
        'liste': liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }

    return render(request, 'monitoring/home.html', context)


def about(request):

    MontageActif = Montage.objects.filter(actif=True)
    salle_navbar = []
    donnees_navbar = []

    for x in MontageActif:
        donnees_navbar.append(
            Donnee_capteur.objects.filter(montage=x.id).last())
        salle_navbar.append(Salle.objects.get(boitier__montage=x.id))

    liste = list(zip(donnees_navbar, salle_navbar))

    context = {
        'title': 'About',
        'liste': liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }

    return render(request, 'monitoring/about.html', context)
