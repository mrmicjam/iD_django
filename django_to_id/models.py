from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Changeset(models.Model):
    created_by = models.ForeignKey(User)
    comment = models.TextField(blank=True, null=True)


class Node(models.Model):
    """Represents a single point"""
    geom = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now = True)
    changeset = models.ForeignKey(Changeset, related_name="nodes")

    objects = models.GeoManager()


class NodeTag(models.Model):
    """key/val tags for nodes"""
    node = models.ForeignKey(Node, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)