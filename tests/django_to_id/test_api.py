from rest_framework.test import APITestCase, APIRequestFactory, APIClient
import unittest
from django_to_id.models import *
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import Point
from django_to_id.serializers import serialize_node


class TestNode(APITestCase):

    def setUp(self):
        self.client = APIClient()

        model_user = User.objects.create_user("micah", "dataconcise@gmail.com", "password")
        model_user.save()

        self.client.force_authenticate(user=model_user)

        pnt = Point(-112.0, 33.4)

        #create the changeset
        model_changeset = Changeset()
        model_changeset.created_by = model_user
        model_changeset.save()
        self.model_changeset = model_changeset

        #create the node
        model_node = Node()
        model_node.changeset = model_changeset
        model_node.geom = pnt
        model_node.save()
        self.model_node = model_node

    def tearDown(self):
        Node.objects.all().delete()
        Changeset.objects.all().delete()
        User.objects.all().delete()

    def test_node_single_record_returned(self):
        url = '/api/0.6/node/%s' % self.model_node.id

        response = self.client.get(url, format='xml')

        returned_data = response.content
        print returned_data
        self.assertTrue(returned_data)

    def test_post_new_node(self):
        data = """
        <osm>
         <node changeset="%s" lat="33.4" lon="-112.1">
           <tag k="note" v="Just a node"/>
         </node>
        </osm>
        """ % self.model_changeset.id
        url = '/api/0.6/node/'
        response = self.client.post(url, data, format='json')
        returned_data = response.content
        self.assertTrue(returned_data)


class TestWay(APITestCase):

    def setUp(self):
        self.client = APIClient()
        model_user = User.objects.create_user("micah", "dataconcise@gmail.com", "password")
        model_user.save()

        self.client.force_authenticate(user=model_user)

        #create the changeset
        model_changeset = Changeset()
        model_changeset.created_by = model_user
        model_changeset.save()
        self.model_changeset = model_changeset

        self.model_way = Way()
        self.model_way.changeset = model_changeset
        self.model_way.save()
        for coord in ((-112.0, 33.4), (-111.8, 33.4), (-111.9, 33.2), (-112.0, 33.4)):
            pnt = Point(-112.0, 33.4)
            #create the node that make a triangle
            model_node = Node()
            model_node.changeset = model_changeset
            model_node.geom = pnt
            model_node.save()
            self.model_way.nodes.add(model_node)

    def test_way_single_record_returned(self):
        url = '/api/0.6/way/%s' % self.model_way.id

        response = self.client.get(url, format='xml')

        returned_data = response.content
        print returned_data
        self.assertTrue(returned_data)
