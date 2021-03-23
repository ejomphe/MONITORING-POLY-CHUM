from django.shortcuts import render
from data_visualization.models import Donnee_capteur, Salle, Montage, Boitier, Climat_exterieur


def listeDepartement(departements):

    departementsUnique = []
    departementsUnique = list(dict.fromkeys(departements))
    print(departementsUnique)

    return departementsUnique


def home(request):

    #MontageActif = (Montage.objects.filter(actif=False))
    MontageActif = Montage.objects.filter(id__in=(1, 2, 3, 4, 5, 6, 17))
    donnees = []
    salles = []
    departements = []
    for x in MontageActif:
        donnees.append(Donnee_capteur.objects.filter(
            montage=x.id, donnee_aberrante=False).last())
        salles.append(Salle.objects.filter(boitier__montage=x.id)[0])
        departements.append(Salle.objects.filter(
            boitier__montage=x.id)[0].departement)

    liste = list(zip(donnees, salles))
    print(liste)
    context = {
        # 'donnees': donnees,
        # 'salles': salles,
        'departements': listeDepartement(departements),
        'liste': liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }

    return render(request, 'monitoring/home.html', context)


# def base(request):
#     context = {
#         'enviroCanada':[Climat_exterieur.objects.last()]
#     }
#     return render(request, 'monitoring/base.html', context)


def about(request):
    return render(request, 'monitoring/about.html', {'title': 'About'})
