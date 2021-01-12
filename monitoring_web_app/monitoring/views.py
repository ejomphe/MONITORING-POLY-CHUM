from django.shortcuts import render

rooms = [
    {
        'roomNumber': '800A',
        'Temp':'25°C',
        'RH': '77%',
        'Pression':'100 atm',
        'Departement':'Rayon X'
    },
    {
        'roomNumber': '800B',
        'Temp':'30°C',
        'RH': '99%',
        'Pression':'104 atm',
        'Departement':'Radio-Oncologie'
    },
     {
        'roomNumber': '800C',
        'Temp':'30°C',
        'RH': '99%',
        'Pression':'104 atm',
        'Departement':'IRM'
    },
     {
        'roomNumber': '800D',
        'Temp':'30°C',
        'RH': '99%',
        'Pression':'104 atm',
        'Departement':'X'
    } 
]

def home(request):
    context = {
        'rooms':rooms
    }
    return render(request, 'monitoring/home.html', context)

def about(request):
    return render(request, 'monitoring/about.html', {'title': 'About'})

def salle1(request):
    return render(request, 'monitoring/800a.html', {'title': 'Salle 800a'})
    
