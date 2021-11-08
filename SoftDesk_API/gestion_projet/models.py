from django.db import models

# Create your models here.
class Projets(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=800, blank=True, null=True)
    type = models.CharField(max_length=250)


class Contributors(models.Model):
    # TODO: changer la liste de choix
    permission = models.CharField(max_length=250, choices={('test','test permission')})
    role = models.CharField(max_length=250)
