from django.urls import path
#from .views import monitoringListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.base, name='base'),
    #path('', views.navtest, name='nav-test'),
    path('about/', views.about, name='about'),
]
