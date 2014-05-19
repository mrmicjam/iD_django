from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import Point, Polygon
from projects.models import Project

class Changeset(models.Model):
    created_by = models.ForeignKey(User)
    comment = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("Changeset", blank=True, null=True)
    project = models.ForeignKey(Project)

class Node(models.Model):
    """Represents a single point"""
    geom = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now=True)
    changeset = models.ForeignKey(Changeset, related_name="nodes")

    parent_id = models.IntegerField(blank=True, null=True)

    objects = models.GeoManager()


class NodeTag(models.Model):
    """key/val tags for nodes"""
    node = models.ForeignKey(Node, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)


class Way(models.Model):
    changeset = models.ForeignKey(Changeset, related_name="ways")
    nodes = models.ManyToManyField(Node, through='WayNodes')
    timestamp = models.DateTimeField(auto_now=True)
    geom = models.PolygonField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)


    def update_geom(self):
        li_coords = []
        for waynode in self.waynodes.all():
            coord = waynode.node.geom.coords
            li_coords.append(coord)

        tpl_coords = tuple(li_coords)
        poly = Polygon(tpl_coords)
        self.geom = poly
        self.save()

    objects = models.GeoManager()

class WayNodes(models.Model):
    way = models.ForeignKey(Way, related_name="waynodes")
    node = models.ForeignKey(Node)
    idx = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = u'osm_api_way_nodes'
        ordering = ['idx']


class WayTag(models.Model):
    """key/val tags for nodes"""
    way = models.ForeignKey(Way, related_name="tags")
    key = models.CharField(max_length=50)
    val = models.CharField(max_length=500)


class Relation(models.Model):
    changeset = models.ForeignKey(Changeset, related_name="relations")
    nodes = models.ManyToManyField(Node, through='RelationToNode')
    ways = models.ManyToManyField(Way, through='RelationToWay')
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
