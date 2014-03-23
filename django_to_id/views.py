from models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from serializers import serialize_node, serialize_way
from rest_framework import status
from BeautifulSoup import BeautifulSoup
from django.contrib.gis.geos.collections import Point
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class ChangeSetViewSetList(APIView):
    """Retrieve a list of changesets or create a new one"""
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        <osm>
          <changeset>
            <tag k="created_by" v="JOSM 1.61"/>
            <tag k="comment" v="Just adding some streetnames"/>
            ...
          </changeset>
          ...
        </osm>"""
        bs = BeautifulSoup(request.DATA)
        xml_node = bs.find('changeset')
        request.user

        lat = float(xml_node.get("lat"))
        lon = float(xml_node.get("lon"))
        pnt = Point(lon, lat)



class NodeViewSet(APIView):
    """
    Retrieve, update or delete a single i9 instance.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        try:
            model_node = Node.objects.get(id=id)
        except:
            return Response("node not found", status=status.status.HTTP_404_NOT_FOUND)

        data = serialize_node(model_node)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)


class NodeViewSetList(APIView):
    """
    Retrieve, update or delete a single i9 instance.
    """

    def post(self, request, format=None):
        """
         <node changeset="12" lat="..." lon="...">
           <tag k="note" v="Just a node"/>
         </node>
        </osm>
        """
        bs = BeautifulSoup(request.DATA)
        xml_node = bs.find('node')

        lat = float(xml_node.get("lat"))
        lon = float(xml_node.get("lon"))
        pnt = Point(lon, lat)
        #create the node
        model_node = Node()
        model_node.changeset_id = int(xml_node.get("changeset"))
        model_node.geom = pnt
        model_node.save()

        kwargs = {'content_type': 'application/json'}
        return HttpResponse(str(model_node.id), **kwargs)


class WayViewSet(APIView):
    """retrieve a single record"""

    def get(self, request, id):
        """
        <osm>
        <way id="5090250" visible="true" timestamp="2009-01-19T19:07:25Z" version="8" changeset="816806" user="Blumpsy" uid="64226">
            <nd ref="822403"/>
            <nd ref="21533912"/>
            <nd ref="821601"/>
            <nd ref="21533910"/>
            <nd ref="135791608"/>
            <nd ref="333725784"/>
            <nd ref="333725781"/>
            <nd ref="333725774"/>
            <nd ref="333725776"/>
            <nd ref="823771"/>
            <tag k="highway" v="residential"/>
            <tag k="name" v="Clipstone Street"/>
            <tag k="oneway" v="yes"/>
        </way>
        </osm>
        """

        try:
            model_way = Way.objects.get(id=id)
        except:
            return Response("node not found", status=status.status.HTTP_404_NOT_FOUND)

        data = serialize_way(model_way)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)


class WayViewSetList(APIView):
    """Retrieve a list of ways, for post a new one"""

    def post(self, request, format=None):
        """
        <osm>
         <way changeset="12">
           <tag k="note" v="Just a way"/>
           ...
           <nd ref="123"/>
           <nd ref="4345"/>
           ...
         </way>
        </osm>
        """

        bs = BeautifulSoup(request.DATA)
        xml_way = bs.find('way')
        model_way = Way()
        model_way.changeset_id = int(xml_way.get("changeset"))
        for nd in xml_way.findall("nd"):
            node_id=int(nd.get("ref"))
            model_way.nodes.add(Node.objects.get(node_id))

        model_way.save()

        for tg in xml_way.find_all("tag"):
            model_way_tag = WayTag()
            model_way_tag.key = tg.get("k")
            model_way_tag.val = tg.get("v")
            model_way_tag.way = model_way
            model_way_tag.save()

        data = serialize_way(model_way)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)

class RelationViewSetList(APIView):

    def post(self, request, format=None):
        """
        <osm>
            <relation id="1" changeset="12">
              <tag k="type" v="multipolygon" />
              <member type="node" role="stop" ref="123"/>
              <member type="way" ref="1" role="outer" />
              <member type="way" ref="2" role="inner" />
              <member type="way" ref="3" role="inner" />
            </relation>
        </osm>
        """

        bs = BeautifulSoup(request.DATA)
        xml_relation = bs.find("relation")
        model_relation = Relation()
        model_relation.changeset_id = int(xml_relation.get("changeset"))
        model_relation.save()
        for member in xml_relation.findall("member"):
            if member.get("type") == "node":
                node_id = int(member.get("ref"))
                role = member.get("role", None)
                RelationToNode.objects.create(relation=model_relation, node=Node.objects.get(node_id), role=role)

            elif member.get("type") == "way":
                way_id = int(member.get("ref"))
                role = member.get("role", None)
                RelationToWay.objects.create(relation=model_relation, way=Way.objects.get(way_id), role=role)

        for tag in xml_relation.findall("tag"):
            RelationTag.objects.create(key = tag.get("k"), val = tag.get("val"))

        data = serialize_relation(model_way)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)



















