from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Changeset(models.Model):
    created_by = models.ForeignKey(User)
    comment = models.TextField(blank=True, null=True)


class Node(models.Model):
    """Represents a single point"""
    geom = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now=True)
    changeset = models.ForeignKey(Changeset, related_name="nodes")

    objects = models.GeoManager()


class NodeTag(models.Model):
    """key/val tags for nodes"""
    node = models.ForeignKey(Node, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)


class Way(models.Model):
    changeset = models.ForeignKey(Changeset, related_name="ways")
    nodes = models.ManyToManyField(Node)
    timestamp = models.DateTimeField(auto_now=True)


class WayTag(models.Model):
    """key/val tags for nodes"""
    way = models.ForeignKey(Way, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)


class Relation(models.Model):
    changeset = models.ForeignKey(Changeset, related_name="relations")
    nodes = models.ManyToManyField(Node, through='RelationToNode')
    ways = models.ManyToManyField(Way,  through='RelationToWay')
    timestamp = models.DateTimeField(auto_now=True)


class RelationTag(models.Model):
    """key/val tags for nodes"""
    relation = models.ForeignKey(Relation, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)


class RelationToWay(models.Model):
    relation = models.ForeignKey(Relation)
    way = models.ForeignKey(Way)
    role = models.CharField(max_length=100)


class RelationToNode(models.Model):
    relation = models.ForeignKey(Relation)
    node = models.ForeignKey(Node)
    role = models.CharField(max_length=100)
