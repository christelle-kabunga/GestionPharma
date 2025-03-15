# creations des routes
from django.urls import path
from .views import *
from . import views  # Import des vues
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Accès à l'interface admin
    path('logout/', LogoutView.as_view(), name='logout'),  # Définition de l'URL pour la déconnexion
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Page de connexion
    path('', login_view, name='login'),  # page login par defaut
    #l’URL pour accéder au tableau de bord.
   path('dashboard/', dashboard, name='dashboard'),

   # avec les vues generiques pour medicament

   path('produit', Affichage.as_view(), name='produit'),
   path('ajout/',ajout_donnees, name='ajout'),
   path('modifier/<uuid:medicament_id>/', modifier_donnees, name='modifier'),
   path('supprimer/<uuid:medicament_id>/', supprimer_donnees, name='supprimer'),
   path('details/<uuid:medicament_id>/', voir_details, name='details'),


# routes pour commande
   path('commandes/', ListeCommandesFournisseurs.as_view(), name='liste_commandes'),
    path('commandes/ajouter/', ajouter_commande, name='ajouter_commande'),
    path('commandes/modifier/<uuid:commande_id>/', modifier_commande, name='modifier_commande'),
    path('commandes/supprimer/<uuid:commande_id>/', supprimer_commande, name='supprimer_commande'),

    # Ventes CRUD
    path('ventes/', views.ventes, name='ventes'),
    path('ajouter/', views.ajouter_vente, name='ajouter_vente'),
    path('modifie/<uuid:vente_id>/', views.modifier_vente, name='modifier_vente'),
    path('supprime/<uuid:vente_id>/', views.supprimer_vente, name='supprimer_vente'),


    # pour les fichiers du template

    path('dashboard', views.dashboard, name='dashboard'),
    path('produit/', views.medicaments, name='produit'),
    path('ventes/', views.ventes, name='ventes'),
    path('commandes/', views.commandes, name='commandes'),
    path('fournisseurs/', views.fournisseurs, name='fournisseurs'),

   # Fournisseur
   path('ajouter/', ajouter_fournisseur, name='ajouter_fournisseur'),
    path('fournisseurs/', views.fournisseurs, name='liste_fournisseurs'),
    path('modf/<uuid:fournisseur_id>/', views.modifier_fournisseur, name='modf'),
    path('supf/<uuid:fournisseur_id>/', views.supprimer_fournisseur, name='supf'),
]