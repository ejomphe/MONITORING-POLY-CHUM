from django.urls import path
from . import views
# Note: il faut commenter cette ligne (qui permet de loader l'app Dash) lors de migration.
from data_visualization.dash_apps import graphs

urlpatterns = [
    path('montage/<nom_montage>/', views.data_visualization,
         name='data-visualization'),

    path('montage/<nom_montage>/info', views.info,
         name='info_montage'),
]
