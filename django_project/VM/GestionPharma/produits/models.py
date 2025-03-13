import uuid
from django.db import models
from django.contrib.auth.models import User

class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'fournisseur'  # Nom de la table dans la base de données

    def __str__(self):
        return self.nom

class Medicament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    date_expiration = models.DateField()

    class Meta:
        db_table = 'medicament'  # Nom de la table dans la base de données

    def statut_quantite(self):
        if self.quantite == 0:
            return 'red'
        elif self.quantite <= 10:
            return 'orange'
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

    class Meta:
        db_table = 'vente'  # Nom de la table dans la base de données

    def __str__(self):
        return f"Vente de {self.quantite} {self.medicament.nom} le {self.date_vente}"

class CommandeFournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_commande = models.DateTimeField(auto_now_add=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)

    class Meta:
        db_table = 'commande_fournisseur'  # Nom de la table dans la base de données

    def __str__(self):
        return f"Commande de {self.quantite} {self.medicament.nom} à {self.fournisseur.nom}"
