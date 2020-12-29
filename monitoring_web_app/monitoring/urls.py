from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='monitoring-home'),
    path('about/', views.about, name='monitoring-about'),

]
