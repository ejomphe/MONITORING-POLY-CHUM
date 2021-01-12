from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<!DOCTYPE html> <html> <body> <h1> <a href="/test-room">Room 800A </a></h1> <p>Temperature: 25C </p> <p>Humidity: 15% </p> <p>Pression 108 mmHg </p> </body> </html>')


def about(request):
    return HttpResponse('<!DOCTYPE html> <html> <head> <title> À propos </title> </head> <body> <h1> À propos</h1> <p>Ce site web a été créé dans le cadre d&#39;un projet scolaire d&#39;étudiants en génie biomédical de Polytechnique Montréal pour le Centre hospitalier de l&#39;Université de Montréal. Celui-ci permet de monitorer, en temps réel, les conditions environnementales dans les salles des départements d&#39;oncologie et de médecine nucléaire du CHUM. Plus précisément, les variables monitorées sont la température, l&#39;humidité relative ainsi que la pression. De plus, les données de météo Canada sont également recueillies pour établir une comparaison avec les conditions environnementales extérieures.</p> <h2>Qui sommes nous</h2> <p> Présentation des 7 étudiants qui ont collaboré sur le projet et les sous-équipes de travail...</p> </body> </html>')