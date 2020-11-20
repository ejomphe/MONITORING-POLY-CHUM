from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<!DOCTYPE html> <html> <body> <h1> Room 800A </h1> <p>Temperature: 25C </p> <p>Humidity: 15% </p> <p>Pression 108 mmHg </p> </body> </html>')

