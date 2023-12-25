from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Recette(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.CharField(max_length=200)
    text_desc = models.CharField(max_length=1000, null=True)

class Commentaire(models.Model):
    texte = models.TextField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


class Ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    rank = models.IntegerField()

class Ingredient(models.Model):
    nom = models.CharField(max_length=200)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)


