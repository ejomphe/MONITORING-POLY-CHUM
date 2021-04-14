from django.shortcuts import render
from .models import Salle,  Climat_exterieur


def data_visualization(request, montage_id):

    if montage_id == "meteo":
        salle = "meteo"
    else:
        salle = Salle.objects.get(
            boitier__montage__pk=montage_id)

    context = {
        'dash_context': {'target_id': {'value': montage_id}},
        'salle': salle,
        'enviroCanada': [Climat_exterieur.objects.last()]
    }
    return render(request, 'data_visualization/base.html', context)
