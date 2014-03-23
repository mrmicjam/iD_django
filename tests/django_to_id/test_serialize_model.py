__author__ = 'micah'
import unittest
from osm_api.models import *
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import Point
from osm_api.serializers import *

class TestSequenceFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        model_user = User.objects.create_user("micah", "dataconcise@gmail.com", "password")
        model_user.save()

        #create the changeset
        model_changeset = Changeset()
        model_changeset.created_by = model_user
        model_changeset.save()
        cls.model_changeset = model_changeset

    def test_serialize_node(self):
        pnt = Point(-112.0, 33.4)
        #create the node
        model_node = Node()
        model_node.changeset = self.model_changeset
        model_node.geom = pnt
        model_node.save()

        xml = serialize_node(model_node)
        self.assertTrue(xml)

    def test_serialize_way(self):
        model_way = Way()
        model_way.changeset = self.model_changeset
        model_way.save()
        for coord in ((-112.0, 33.4), (-111.8, 33.4), (-111.9, 33.2), (-112.0, 33.4)):
            pnt = Point(*coord)
            #create the node that make a triangle
            model_node = Node()
            model_node.changeset = self.model_changeset
            model_node.geom = pnt
            model_node.save()
            model_way.nodes.add(model_node)
        xml = serialize_way(model_way)
        self.assertTrue(xml)

    def test_serialize_relation(self):
        model_way = Way()
        model_way.changeset = self.model_changeset
        model_way.save()
        for coord in ((-112.0, 33.4), (-111.8, 33.4), (-111.9, 33.2), (-112.0, 33.4)):
            pnt = Point(*coord)
            #create the node that make a triangle
            model_node = Node()
            model_node.changeset = self.model_changeset
            model_node.geom = pnt
            model_node.save()
            model_way.nodes.add(model_node)

        model_relation = Relation()
        model_relation.changeset = self.model_changeset
        model_relation.save()

        RelationToWay.objects.create(relation=model_relation, way=model_way, role="outer")
        xml = serialize_relation(model_relation)
        print xml
        self.assertTrue(xml)






