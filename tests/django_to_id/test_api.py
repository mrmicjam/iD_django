from rest_framework.test import APITestCase, APIRequestFactory, APIClient
import unittest
from django_to_id.models import *
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import Point
from django_to_id.serializers import serialize_node


class I9Tests(APITestCase):

    def setUp(self):
        self.client = APIClient()
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

    def test_i9_single_record_returned(self):
        url = '/api/0.6/node/%s' % self.model_node.id

        response = self.client.get(url, format='xml')

        returned_data = response.content
        print returned_data
        self.assertTrue(returned_data)