from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
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

    def __str__(self):
        return  'id : ' + str(self.id) + ' - title : ' + str(self.title)

class Contributors(models.Model):

    PERMISSIONS_CHOICES = (
        ("1","author"),
        ("2", "contributor"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contrib', on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    # TODO : permissions choices
    permission = models.CharField(max_length=250, choices=PERMISSIONS_CHOICES)
    role = models.CharField(max_length=250)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = _('Contributor')
        verbose_name_plural = _('Contributors')

    def __str__(self):
        return str(self.user)

class Issues(models.Model):
    title = models.CharField(max_length=250)
    project_id = models.ForeignKey(Projects, related_name='project', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)

    description = models.CharField(max_length=350, blank=True, null=True)
    tag = models.CharField(max_length=150, blank=True, null=True)
    priority =models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assignee_user', on_delete=SET_NULL, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')


class Comments(models.Model):
    description = models.CharField(max_length = 250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
