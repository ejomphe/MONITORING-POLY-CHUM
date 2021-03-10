from django.shortcuts import render
from data_visualization.models import Donnee_capteur
from data_visualization.models import Salle
from data_visualization.models import Montage
from data_visualization.models import Boitier
from data_visualization.models import Climat_exterieur

def listeDepartement(departements):

    departementsUnique = []
    departementsUnique = list(dict.fromkeys(departements))
    print(departementsUnique) 
            
    return departementsUnique


def home(request):
    
    #MontageActif = (Montage.objects.filter(actif=False))
    MontageActif = Montage.objects.all()
    donnees = []
    salles = []
    departements = []
    for x in MontageActif:
        donnees.append(Donnee_capteur.objects.filter(montage = x.id).last())
        salles.append(Salle.objects.filter(boitier__montage = x.id)[0])
        departements.append(Salle.objects.filter(boitier__montage = x.id)[0].departement)

    liste = list(zip(donnees, salles))
    context = {
        'donnees':donnees, 
        'salles':salles, 
        'departements':listeDepartement(departements), 
        'liste':liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
        }

    return render(request, 'monitoring/home.html', context)


def base(request):
    context = {
        'enviroCanada':[Climat_exterieur.objects.last()]
    }
    return render(request, 'monitoring/base.html', context)


def about(request):
    return render(request, 'monitoring/about.html', {'title': 'About'})


def salle1(request):
    return render(request, 'monitoring/800a.html', {'roomNumber': 'Salle 800A'})
