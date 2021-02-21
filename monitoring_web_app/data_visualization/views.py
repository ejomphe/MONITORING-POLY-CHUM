from django.shortcuts import render
from .models import Salle


def test_room(request, montage_id):

    if montage_id == "meteo":
        salle = "meteo"
    else:
        salle = Salle.objects.filter(
            boitier__montage__donnee_capteur__montage=montage_id).last()

    context = {
        'dash_context': {'target_id': {'value': montage_id}},
        'salle': salle
    }
    return render(request, 'data_visualization/base.html', context)
