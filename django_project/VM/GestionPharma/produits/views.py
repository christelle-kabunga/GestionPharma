from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login
import uuid
from .models import *
from datetime import datetime


#appel des fichiers templates

def dashboard(request):
    return render(request, 'home.html')

def medicaments(request):
    liste_medicaments = Medicament.objects.all()  # Récupérer tous les médicaments
    return render(request, 'produit.html', {'medicaments': liste_medicaments})

def ventes(request):
    ventes = Vente.objects.all()
    return render(request, 'ventes.html',{'ventes': ventes})

def commandes(request):
    return render(request, 'commandes.html')

def fournisseurs(request):
    liste_fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur.html',{'fournisseurs': liste_fournisseurs})


#pour vérifier si l'utilisateur est un superutilisateur

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Vérification des identifiants
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Connecte l'utilisateur
            return redirect('dashboard')  # Redirige vers la page d'accueil
        else:
            return render(request, 'login.html', {'error': 'Identifiants invalides'})
    
    return render(request, 'login.html')

#deconnexion
def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion

# Affichage des médicaments avec ListView
class Affichage(ListView):
    template_name = 'produit.html'  # Template utilisé
    model = Medicament  # Modèle associé
    context_object_name = 'donnees'  # Nom de la variable dans le template

# Fonction d'ajout de médicaments
def ajout_donnees(request):
    
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            description = request.POST.get('description', '')
            prix = request.POST.get('prix')
            quantite = request.POST.get('quantite')
            date_expiration = request.POST.get('date_expiration')

            # Vérifier si tous les champs obligatoires sont remplis
            if not (nom and prix and quantite and date_expiration):
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                return render(request, "add-product.html")

            # Convertir prix et quantite en nombres (gestion d'erreur)
            try:
                prix = float(prix)
                quantite = int(quantite)
            except ValueError:
                messages.error(request, "Prix ou quantité incorrects. Veuillez entrer des valeurs valides.")
                return render(request, "add-product.html")
            
            #validation de la date

            try:
                date_expiration = datetime.strptime(date_expiration, '%Y-%m-%d')
            except ValueError:
                messages.error(request, "Le format de la date n'est pas bon. Essayez avec ceci AAAA/MM/JJ")
                return render(request, "add-product.html")

            #validation prix
            try:
                prix = float(prix)

                if prix <= 0:
                    messages.error(request, "Le prix n'est doit pas être négatif ou égal à 0")
                    return render(request, "add-product.html")

            except ValueError:
                messages.error(request, "Entrez un prix valide svp!")
                return render(request, "add-product.html")
             
            # Enregistrement dans MySQL
            Medicament.objects.create(
                id=uuid.uuid4(),
                nom=nom,
                description=description,
                prix=prix,
                quantite=quantite,
                date_expiration=date_expiration
            )

        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du produit : {e}")
            return render(request, "add-product.html")

        # Si tout s'est bien passé, afficher le message de succès et rediriger
        messages.success(request, "Produit ajouté avec succès !")
        return redirect('produit')  

    else:
        return render(request, "add-product.html")
# Fonction de modification d'un médicament
def modifier_donnees(request, medicament_id):
    try:
        medicament_uuid = uuid.UUID(str(medicament_id))  # 🔹 Convertir en UUID
    except ValueError:
        messages.error(request, "Identifiant invalide.")
        return redirect('produit')

    medicament = get_object_or_404(Medicament, id=medicament_uuid)  # 🔹 Recherche avec UUID

    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            description = request.POST.get('description', '')
            prix = request.POST.get('prix')
            quantite = request.POST.get('quantite')
            date_expiration = request.POST.get('date_expiration')

            # Vérifier si tous les champs obligatoires sont remplis
            if not (nom and prix and quantite and date_expiration):
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                return render(request, "edit-product.html", {"medicament": medicament})

            # Convertir prix et quantite en nombres (gestion d'erreur)
            try:
                prix = float(prix)
                quantite = int(quantite)
                if prix <= 0:
                    raise ValueError("Le prix doit être positif.")
                if quantite < 0:
                    raise ValueError("La quantité ne peut pas être négative.")
            except ValueError as e:
                messages.error(request, str(e))
                return render(request, "edit-product.html", {"medicament": medicament})

            # Validation et conversion de la date
            try:
                date_expiration = datetime.strptime(date_expiration, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Le format de la date est incorrect. Utilisez AAAA-MM-JJ.")
                return render(request, "edit-product.html", {"medicament": medicament})

            # Mise à jour du médicament
            medicament.nom = nom
            medicament.description = description
            medicament.prix = prix
            medicament.quantite = quantite
            medicament.date_expiration = date_expiration
            medicament.save()

            messages.success(request, "Produit modifié avec succès !")
            return redirect('produit')

        except Exception as e:
            messages.error(request, f"Erreur lors de la modification du produit : {e}")
            return render(request, "edit-product.html", {"medicament": medicament})

    return render(request, "edit-product.html", {"medicament": medicament})

# Fonction de suppression
def supprimer_donnees(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    
    if request.method == "POST":
        medicament.delete()
        messages.success(request, "Médicament supprimé avec succès !")
        return redirect('produit')

    return render(request, "delete-confirmation.html", {"medicament": medicament})

# Fonction pour afficher les détails d'un médicament
def voir_details(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    return render(request, "details.html", {"medicament": medicament})


#  Liste des commandes
class ListeCommandesFournisseurs(ListView):
    template_name = 'commandes.html'
    model = CommandeFournisseur
    context_object_name = 'commandes'

#  Ajouter une commande fournisseur
def ajouter_commande(request):
    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')

        if not (medicament_id and quantite and fournisseur_id):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('ajouter_commande')

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError("La quantité doit être un nombre positif.")

            medicament = get_object_or_404(Medicament, id=medicament_id)
            fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

            CommandeFournisseur.objects.create(
                id=uuid.uuid4(),
                medicament=medicament,
                quantite=quantite,
                fournisseur=fournisseur
            )

            messages.success(request, "Commande ajoutée avec succès !")
            return redirect('liste_commandes')

        except ValueError:
            messages.error(request, "Quantité invalide.")
            return redirect('ajouter_commande')

    medicaments = Medicament.objects.all()
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'ajouter_commande.html', {'medicaments': medicaments, 'fournisseurs': fournisseurs})

#  Modifier une commande fournisseur
def modifier_commande(request, commande_id):
    commande = get_object_or_404(CommandeFournisseur, id=commande_id)

    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')

        if not (medicament_id and quantite and fournisseur_id):
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('modifier_commande', commande_id=commande_id)

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError("La quantité doit être un nombre positif.")

            medicament = get_object_or_404(Medicament, id=medicament_id)
            fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

            commande.medicament = medicament
            commande.quantite = quantite
            commande.fournisseur = fournisseur
            commande.save()

            messages.success(request, "Commande modifiée avec succès !")
            return redirect('liste_commandes')

        except ValueError:
            messages.error(request, "Quantité invalide.")
            return redirect('modifier_commande', commande_id=commande_id)

    medicaments = Medicament.objects.all()
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'modifier_commande.html', {'commande': commande, 'medicaments': medicaments, 'fournisseurs': fournisseurs})

#  Supprimer une commande fournisseur
def supprimer_commande(request, commande_id):
    commande = get_object_or_404(CommandeFournisseur, id=commande_id)

    if request.method == "POST":
        commande.delete()
        messages.success(request, "Commande supprimée avec succès !")
        return redirect('liste_commandes')

    return render(request, "supprimer_commande.html", {"commande": commande})

# Ajout d'un fournisseur
def ajouter_fournisseur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse', '')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')

        if not (nom and telephone and email):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('ajouter_fournisseur')

        if Fournisseur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('ajouter_fournisseur')

        # Création du fournisseur
        Fournisseur.objects.create(
            nom=nom,
            adresse=adresse,
            telephone=telephone,
            email=email
        )

        messages.success(request, "Fournisseur ajouté avec succès !")
        return redirect('liste_fournisseurs')

    return render(request, 'ajouter_fournisseur.html')

# Modification d'un fournisseur
def modifier_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

    if request.method == 'POST':
        fournisseur.nom = request.POST.get('nom')
        fournisseur.adresse = request.POST.get('adresse', '')
        fournisseur.telephone = request.POST.get('telephone')
        fournisseur.email = request.POST.get('email')

        if Fournisseur.objects.exclude(id=fournisseur_id).filter(email=fournisseur.email).exists():
            messages.error(request, "Cet email est déjà utilisé par un autre fournisseur.")
            return redirect('modifier_fournisseur', fournisseur_id=fournisseur_id)

        fournisseur.save()
        messages.success(request, "Fournisseur modifié avec succès !")
        return redirect('liste_fournisseurs')

    return render(request, 'modifier_fournisseur.html', {'fournisseur': fournisseur})

# Suppression d'un fournisseur
def supprimer_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)

    if request.method == "POST":
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé avec succès !")
        return redirect('liste_fournisseurs')

    return render(request, "supprimer_fournisseur.html", {"fournisseur": fournisseur})
# ===================== GESTION DES VENTES ===================== #
@login_required
def ajouter_vente(request):
    """ Ajoute une nouvelle vente après vérification des stocks. """
    if request.method == 'POST':
        medicament_id = request.POST.get('medicament')
        quantite = request.POST.get('quantite')

        if not (medicament_id and quantite):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('ajouter_vente')

        try:
            quantite = int(quantite)
            if quantite <= 0:
                raise ValueError("La quantité doit être un nombre positif.")

            medicament = get_object_or_404(Medicament, id=medicament_id)
            
            if medicament.quantite < quantite:
                messages.error(request, "Stock insuffisant pour cette vente.")
                return redirect('ajouter_vente')

            Vente.objects.create(
                id=uuid.uuid4(),
                medicament=medicament,
                quantite=quantite,
                vendu_par=request.user
            )
            
            medicament.quantite -= quantite  # Réduction du stock
            medicament.save()

            messages.success(request, "Vente enregistrée avec succès !")
            return redirect('ventes')

        except ValueError:
            messages.error(request, "Quantité invalide.")
            return redirect('ajouter_vente')

    medicaments = Medicament.objects.all()
    return render(request, 'ajouter_vente.html', {'medicaments': medicaments})

@login_required
def modifier_vente(request, vente_id):
    """ Modifie une vente existante. """
    vente = get_object_or_404(Vente, id=vente_id)
    if request.method == 'POST':
        try:
            nouvelle_quantite = int(request.POST.get('quantite'))
            if nouvelle_quantite <= 0:
                raise ValueError("Quantité invalide.")
            
            difference = nouvelle_quantite - vente.quantite
            if vente.medicament.quantite < difference:
                messages.error(request, "Stock insuffisant pour cette modification.")
                return redirect('modifier_vente', vente_id=vente.id)

            vente.medicament.quantite -= difference
            vente.medicament.save()

            vente.quantite = nouvelle_quantite
            vente.save()

            messages.success(request, "Vente modifiée avec succès !")
            return redirect('ventes')
        except ValueError:
            messages.error(request, "Veuillez entrer une quantité valide.")
            return redirect('modifier_vente', vente_id=vente.id)
    return render(request, 'modifier_vente.html', {'vente': vente})

@login_required
def supprimer_vente(request, vente_id):
    """ Supprime une vente existante et remet les médicaments en stock. """
    vente = get_object_or_404(Vente, id=vente_id)
    vente.medicament.quantite += vente.quantite  # Rétablissement du stock
    vente.medicament.save()
    if request.method == "POST":
        vente.delete()
        messages.success(request, "Vente supprimée avec succès !")
        return redirect('ventes')

    return render(request, "supprimer_vente.html", {"vente": vente})
# Affiche la liste des ventes.
@login_required
def liste_ventes(request):
    """ Affiche la liste des ventes. """
    ventes = Vente.objects.all()
    total = sum(vente.medicament.prix * vente.quantite for vente in ventes)  # Calcul du total
    return render(request, 'ventes.html', {'ventes': ventes,'total': total})


#fonction pour passer le total des ventes et d'autres totaux au template
@login_required
def dashboard(request):
    """ Affiche le tableau de bord avec les totaux """
    
    # Vérifie si la base de données contient des données avant de faire les calculs
    total_ventes = Vente.objects.aggregate(total=models.Sum(models.F('medicament__prix') * models.F('quantite')))['total'] or 0
    total_medicaments = Medicament.objects.count()
    total_fournisseurs = Fournisseur.objects.count()
    total_commandes = CommandeFournisseur.objects.count()

    context = {
        'total_ventes': total_ventes,
        'total_medicaments': total_medicaments,
        'total_fournisseurs': total_fournisseurs,
        'total_commandes': total_commandes
    }
    return render(request, 'home.html', context)