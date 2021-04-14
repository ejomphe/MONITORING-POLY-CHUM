from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .utils.utils import auto_email_task

# Create your views here.


def alert(request):

    auto_email_task()

    return HttpResponse("Vérification alertes faite")
