import uuid
from django.db import models
from django.contrib.auth.models import User

class Medicament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    date_expiration = models.DateField()

    def statut_quantite(self):
        #si la quantite est égale à affiche rouge
        if self.quantite == 0:
            return 'red'
        
        #sinon si la quantité est infereur ou egale à 10 affiche orange

        elif self.quantite <= 10:
            return 'orange'
        
        #sinon orange
        else:
            return 'green'
    def __str__(self):
        return self.nom

class Vente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_vente = models.DateTimeField(auto_now_add=True)
    vendu_par = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Vente de {self.quantite} {self.medicament.nom} le {self.date_vente}"

class CommandeFournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_commande = models.DateTimeField(auto_now_add=True)
    fournisseur = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Commande de {self.quantite} {self.medicament.nom} à {self.fournisseur}"