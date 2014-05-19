from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name="projects")
    starting_point = models.PointField(srid=4326, blank=True, null=True)

    objects = models.GeoManager()


class UserToProject(models.Model):
    proj = models.ForeignKey(Project)
    user = models.ForeignKey(User, blank=True, null=True, related_name="subscribed_projects")
    dt_invited = models.DateTimeField(auto_now_add=True)
    invitation_email = models.EmailField()


