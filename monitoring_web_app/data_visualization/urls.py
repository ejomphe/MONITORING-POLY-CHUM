from django.urls import path
from . import views
# Note: il faut commenter cette ligne (qui permet de loader l'app Dash) lors de migration.
from data_visualization.dash_apps import graphs

urlpatterns = [
    path('montage/<montage_id>/', views.data_visualization,
         name='data-visualization'),
]
