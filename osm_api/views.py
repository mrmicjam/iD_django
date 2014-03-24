from models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from serializers import serialize_node, serialize_way, serialize_relation, serialize_map
from rest_framework import status
from BeautifulSoup import BeautifulSoup
from django.contrib.gis.geos.collections import Point
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Polygon


# TODO: capabilites
# http://www.openstreetmap.org/api/capabilities
"""
<?xml version="1.0" encoding="UTF-8"?>
<osm version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
  <api>
    <version minimum="0.6" maximum="0.6"/>
    <area maximum="0.25"/>
    <tracepoints per_page="5000"/>
    <waynodes maximum="2000"/>
    <changesets maximum_elements="50000"/>
    <timeout seconds="300"/>
    <status database="online" api="online" gpx="online"/>
  </api>
</osm>
"""

def capabilities(request):
    xml_data = """<osm version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
                  <api>
                    <version minimum="0.6" maximum="0.6"/>
                    <area maximum="0.25"/>
                    <tracepoints per_page="5000"/>
                    <waynodes maximum="2000"/>
                    <changesets maximum_elements="50000"/>
                    <timeout seconds="300"/>
                    <status database="online" api="online" gpx="online"/>
                  </api>
                </osm>"""
    kwargs = {'content_type': 'application/xml'}
    return HttpResponse(xml_data, **kwargs)




# http://taginfo.openstreetmap.org/api/4/key/values?key=building&page=1&rp=20&sortname=count_all&sortorder=desc
# {"page":1,"rp":20,"total":5480,"data":[{"value":"yes","count":96787186,"fraction":0.8966000000000001,"in_wiki":true,"description":""},{"value":"house","count":4444942,"fraction":0.0412,"in_wiki":true,"description":"A single dwelling unit usually inhabited by one family."},{"value":"residential","count":1888321,"fraction":0.0175,"in_wiki":true,"description":"A general tag for a building used primarily for residential purposes."},{"value":"garage","count":900410,"fraction":0.0083,"in_wiki":true,"description":"Denotes a single-owner private garage"},{"value":"hut","count":767523,"fraction":0.0071,"in_wiki":true,"description":"A small and crude shelter."},{"value":"apartments","count":568824,"fraction":0.0053,"in_wiki":true,"description":"A building arranged into individual dwellings, often on separate floors. May also have retail outlets on the ground floor."},{"value":"industrial","count":360133,"fraction":0.0033,"in_wiki":true,"description":"A building where some industrial process takes place."},{"value":"roof","count":287102,"fraction":0.0027,"in_wiki":true,"description":"To enter roofs opened on at least two sides."},{"value":"garages","count":212905,"fraction":0.002,"in_wiki":true,"description":"A block of private garages each with a separate owner"},{"value":"detached","count":139192,"fraction":0.0013000000000000002,"in_wiki":true,"description":"A free-standing residential building usually housing a single-family."},{"value":"terrace","count":129296,"fraction":0.0012000000000000001,"in_wiki":true,"description":"A single way used to define the outline of a linear row of residential dwellings, each of which normally has its own entrance, which form a terrace (\"row-house\" or \"townhouse\" in North American English)."},{"value":"entrance","count":118582,"fraction":0.0011,"in_wiki":true,"description":"To mark the location of a building entrance."},{"value":"farm_auxiliary","count":117780,"fraction":0.0011,"in_wiki":true,"description":"A building on a farm that is not a dwelling."},{"value":"school","count":99295,"fraction":0.0009000000000000001,"in_wiki":true,"description":"A generic school building."},{"value":"commercial","count":96800,"fraction":0.0009000000000000001,"in_wiki":true,"description":"A building where non-specific commercial activities take place."},{"value":"retail","count":85331,"fraction":0.0008,"in_wiki":true,"description":"A building primarily used for selling goods to the general public."},{"value":"church","count":80562,"fraction":0.0007,"in_wiki":true,"description":"A building that was built as a church."},{"value":"shed","count":69194,"fraction":0.0006000000000000001,"in_wiki":true,"description":"A small, simple structure used as storage or workshop"},{"value":"service","count":62902,"fraction":0.0006000000000000001,"in_wiki":false,"description":""},{"value":"manufacture","count":59941,"fraction":0.0006000000000000001,"in_wiki":true,"description":""}]}

#http://www.openstreetmap.org/api/0.6/user/details
"""
<osm version="0.6" generator="OpenStreetMap server">
  <user id="1727933" display_name="Micah Jamison" account_created="2013-08-28T16:32:26Z">
    <description></description>
    <contributor-terms agreed="true" pd="false"/>
    <img href="http://www.gravatar.com/avatar/21783945d024acff7aa3131a34bf0ac2.jpg?s=256&amp;d=http%3A%2F%2Fwww.openstreetmap.org%2Fassets%2Fusers%2Fimages%2Flarge-82d94ac521dc6dc7a27fee5c8aa13901.png"/>
    <roles>
    </roles>
    <changesets count="0"/>
    <traces count="0"/>
    <blocks>
      <received count="0" active="0"/>
    </blocks>
    <languages>
      <lang>en-US</lang>
      <lang>en</lang>
    </languages>
    <messages>
      <received count="0" unread="0"/>
      <sent count="0"/>
    </messages>
  </user>
</osm>
"""

#http://www.openstreetmap.org/api/0.6/changeset/create
#response: 21273202

#http://www.openstreetmap.org/api/0.6/changeset/21273202/upload
#request
"""
<osmChange version="0.3" generator="iD"><create><node id="-1" lon="-77.02499373670848" lat="38.90390890643066" version="0" changeset="21273202"/><node id="-4" lon="-77.02523116726093" lat="38.90389400295947" version="0" changeset="21273202"/><node id="-7" lon="-77.0247056594091" lat="38.903893960972944" version="0" changeset="21273202"/><node id="-10" lon="-77.02472486456239" lat="38.90344559577833" version="0" changeset="21273202"/><node id="-13" lon="-77.02528181400784" lat="38.903490432425194" version="0" changeset="21273202"/><way id="-1" version="0" changeset="21273202"><nd ref="-1"/><nd ref="-4"/><nd ref="-7"/><nd ref="-10"/><nd ref="-13"/><nd ref="-1"/><tag k="landuse" v="industrial"/></way></create><modify><way id="55316596" version="3" changeset="21273202"><nd ref="694858819"/><nd ref="694859354"/><nd ref="694859524"/><nd ref="-4"/><nd ref="694860182"/><nd ref="694860755"/><nd ref="694858819"/><tag k="building" v="yes"/><tag k="dcgis:captureyear" v="19990331"/><tag k="dcgis:dataset" v="buildings"/><tag k="dcgis:featurecode" v="2000"/><tag k="source" v="dcgis"/></way></modify><delete if-unused="true"/></osmChange>
"""
#response
"""<?xml version="1.0" encoding="UTF-8"?>
<diffResult version="0.6" generator="OpenStreetMap server" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
  <node old_id="-1" new_id="2737987605" new_version="1"/>
  <node old_id="-4" new_id="2737987611" new_version="1"/>
  <node old_id="-7" new_id="2737987615" new_version="1"/>
  <node old_id="-10" new_id="2737987619" new_version="1"/>
  <node old_id="-13" new_id="2737987622" new_version="1"/>
  <way old_id="-1" new_id="268458792" new_version="1"/>
  <way old_id="55316596" new_id="55316596" new_version="4"/>
</diffResult>
"""

#http://www.openstreetmap.org/api/0.6/changeset/21273202/close


# TODO: map bbox view
# connection.js:282
# http://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_map_data_by_bounding_box:_GET_.2Fapi.2F0.6.2Fmap
# '/api/0.6/map?bbox=' + [b[0][0], b[1][1], b[1][0], b[0][1]];
# ex: http://www.openstreetmap.org/api/0.6/map?bbox=-112.101,33.21,-112.01,33.22
class MapViewSet(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, left, bottom, right, top):
        poly = Polygon(((left, bottom), (left, top), (right, top), (right, bottom), (left, bottom)))
        nodes = Node.objects.filter(geom__within=poly)
        xml = serialize_map(poly, nodes)



#TODO Changeset view
#connection.js:227
# PUT: '/api/0.6/changeset/create'
# POST: '/api/0.6/changeset/' + changeset_id + '/upload',
# PUT: '/api/0.6/changeset/' + changeset_id + '/close'
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
            return Response("way not found", status=status.status.HTTP_404_NOT_FOUND)

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


class RelationViewSet(APIView):
    """retrieve a single record"""

    def get(self, request, id):
        """
        see serializers.py for example relation xml
        """

        try:
            model_relation = Relation.objects.get(id=id)
        except:
            return Response("relation not found", status=status.status.HTTP_404_NOT_FOUND)

        data = serialize_relation(model_relation)
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

        data = serialize_relation(model_relation)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)


class MapViewSet(APIView):


    def get(self, request):
        #define the map boundaries
        left, bottom, right, top = [float(x) for x in request.GET.keys()[0].split(",")]
        poly = Polygon(((left, bottom), (left, top), (right, top), (right, bottom), (left, bottom)))
        nodes = Node.objects.filter(geom__within=poly)

        data = serialize_map((left, bottom, right, top), nodes)
        kwargs = {'content_type': 'application/json'}
        return HttpResponse(data, **kwargs)


















