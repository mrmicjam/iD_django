__author__ = 'micah'
import unittest
from django_to_id.models import *
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import Point
from django_to_id.serializers import serialize_node


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        model_user = User.objects.create_user("micah", "dataconcise@gmail.com", "password")
        model_user.save()
        pnt = Point(-112.0, 33.4)

        #create the changeset
        model_changeset = Changeset()
        model_changeset.created_by = model_user
        model_changeset.save()

        #create the node
        model_node = Node()
        model_node.changeset = model_changeset
        model_node.geom = pnt
        model_node.save()
        self.model_node = model_node

    def test_serialize_node(self):
        xml = serialize_node(self.model_node)
        self.assertTrue(xml)


