from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
import uuid
from .models import Medicament
from datetime import datetime

# Affichage des médicaments avec ListView
class Affichage(ListView):
    template_name = 'home.html'  # Template utilisé
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
        return redirect('ajout')  

    else:
        return render(request, "add-product.html")
# Fonction de modification d'un médicament
def modifier_donnees(request, medicament_id):
    try:
        medicament_uuid = uuid.UUID(str(medicament_id))  # 🔹 Convertir en UUID
    except ValueError:
        messages.error(request, "Identifiant invalide.")
        return redirect('home')

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
            return redirect('home')

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
        return redirect('home')

    return render(request, "delete-confirmation.html", {"medicament": medicament})

# Fonction pour afficher les détails d'un médicament
def voir_details(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    return render(request, "details.html", {"medicament": medicament})
