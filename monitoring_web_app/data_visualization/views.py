from django.shortcuts import render

def test_room(request):
    return render(request, 'data_visualization/base.html', {'title':'800A'})  #éventuellement le numéro de la salle devra être passé automatiquement... créer une fonction qui va lire dans BD...
