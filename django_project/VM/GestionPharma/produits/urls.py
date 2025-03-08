# creations des routes
from django.urls import path
from .views import *

urlpatterns = [
   # path('',home, name='home'),

   # avec les vues generiques

   path('', Affichage.as_view(), name='home'),
   path('ajout/',ajout_donnees, name='ajout'),
   path('modifier/<uuid:medicament_id>/', modifier_donnees, name='modifier'),
   path('supprimer/<uuid:medicament_id>/', supprimer_donnees, name='supprimer'),
   path('details/<uuid:medicament_id>/', voir_details, name='details'),
]