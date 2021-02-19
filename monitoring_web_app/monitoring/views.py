from django.shortcuts import render
from data_visualization.models import Donnee_capteur


def home(request):
    context = {
        # TODO: créer fonction qui va récupérer automatiquement les id des montages actifs
        # TODO: mettre une clé 'salle' dans le contexte contenant une liste des salles associées aux montages pour affichage sur home.
        'rooms': [Donnee_capteur.objects.filter(montage=1).last(), Donnee_capteur.objects.filter(montage=2).last(), Donnee_capteur.objects.filter(montage=3).last()]
    }
    return render(request, 'monitoring/home.html', context)


def about(request):
    return render(request, 'monitoring/about.html', {'title': 'About'})
