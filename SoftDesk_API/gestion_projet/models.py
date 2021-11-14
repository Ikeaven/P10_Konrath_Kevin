from django.db import models
from django.db.models.deletion import CASCADE

from authentication.models import User

# Create your models here.
class Projets(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=800, blank=True, null=True)
    type = models.CharField(max_length=250)
    # TODO : passer l'author en manyToMany
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Contributors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projets, on_delete=models.CASCADE)
    # TODO : permissions choices
    permission = models.CharField(max_length=250, choices={('test','test permission')})
    role = models.CharField(max_length=250)
