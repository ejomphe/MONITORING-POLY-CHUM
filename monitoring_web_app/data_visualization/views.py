from django.shortcuts import render
from .models import Salle


def data_visualization(request, montage_id):

    if montage_id == "meteo":
        salle = "meteo"
    else:
        salle = Salle.objects.filter(
            boitier__montage__pk=montage_id)[0]

    context = {
        'dash_context': {'target_id': {'value': montage_id}},
        'salle': salle
    }
    return render(request, 'data_visualization/base.html', context)
