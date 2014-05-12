from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)


class UserToProject(models.Model):
    proj = models.ForeignKey(Project)
    user = models.ForeignKey(User, blank=True, null=True)
    dt_invited = models.DateTimeField(auto_now_add=True)
    invitation_email = models.EmailField()


