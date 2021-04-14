from django.shortcuts import render
from data_visualization.models import Donnee_capteur, Salle, Montage, Boitier, Climat_exterieur
from alert.utils.utils import check_for_alert


def listeDepartement(departements):

    departementsUnique = []
    departementsUnique = list(dict.fromkeys(departements))
            
    return departementsUnique


def home(request):
    
    MontageActif = (Montage.objects.filter(actif=True))
    salles = []
    departements = []
    donnees = []
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
            # TODO ajouter vérification de la dernière données pour chaque salle pour envoie alerte.
            #check_for_alert(derniere_donnee, salle)

            departements.append(Salle.objects.get(
                boitier__montage__pk=x.id).departement)

    liste = list(zip(donnees, salles))

    context = { 
        'salle_navbar':salles, 
        'departements':listeDepartement(departements), 
        'liste':liste,
        'enviroCanada': [Climat_exterieur.objects.last()]
        }
    

    return render(request, 'monitoring/home.html', context)


def about(request):
    return render(request, 'monitoring/about.html', {'title': 'About'})
