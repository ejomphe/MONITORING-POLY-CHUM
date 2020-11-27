from django.shortcuts import render
from django.http import HttpResponse


##Deuxième facon
def home(request):
    return render(request, 'monitoring/general_home.html')