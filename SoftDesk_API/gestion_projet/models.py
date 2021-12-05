from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# from django.db.models.deletion import CASCADE

# from authentication.models import User


class Projects(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=800, blank=True, null=True)
    type = models.CharField(max_length=250)
    # TODO : passer l'author en manyToMany
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE, null=True)
    contributor = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributors', related_name='contributions')

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

class Contributors(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    # TODO : permissions choices
    permission = models.CharField(max_length=250, choices={('test', 'test permission')})
    role = models.CharField(max_length=250)

    class Meta:
        unique_together = ('user', 'project')
