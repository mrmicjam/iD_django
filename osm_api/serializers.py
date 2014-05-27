__author__ = 'micah'

from lxml import etree
from models import RelationToWay, RelationToNode, WayNodes, Way, Relation, Node, Changeset
from django.contrib.gis.geos import Polygon

"""
<osm>
<node id="25496583" lat="51.5173639" lon="-0.140043" version="1" changeset="203496" user="80n" uid="1238" visible="true" timestamp="2007-01-28T11:40:26Z">
    <tag k="highway" v="traffic_signals"/>
</node>
</osm>
"""

def serialize_node(model_node, envelope=True, return_format="string"):
    """
    Given a model_node, return it per http://wiki.openstreetmap.org/wiki/API_v0.6#Response_12
    """
    lon, lat = model_node.geom.coords

    # another child with text
    child = etree.Element('node', id=str(model_node.id), changeset=str(model_node.changeset.id), lat=str(lat), lon=str(lon),
                          timestamp=model_node.timestamp.isoformat() + "Z", visible="true", uid=str(model_node.changeset.created_by.id),
                          user=model_node.changeset.created_by.username, version="1")

    for model_tag in model_node.tags.all():
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    if envelope:
        # create XML
        root = etree.Element('osm')
        root.append(child)
    else:
        root = child

    if return_format == "string":
        # pretty string
        s = etree.tostring(root, pretty_print=True)
        return s
    else:
        return root


def serialize_way(model_way, envelope=True, filter_nodes_ids=None, return_format="string"):
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


    # another child with text
    child = etree.Element('way', id=str(model_way.id), changeset=str(model_way.changeset.id),
                          user=model_way.changeset.created_by.username, uid=str(model_way.changeset.created_by.id),
                          timestamp=model_way.timestamp.isoformat() + "Z", visible="true", version="1")

    for model_tag in model_way.tags.all():
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    qry_waynodes = WayNodes.objects.filter(way = model_way)

    for waynode in qry_waynodes:
        node = waynode.node
        node_child = etree.Element('nd', ref=str(node.id))
        child.append(node_child)

    if envelope:
        # create XML
        root = etree.Element('osm')
        root.append(child)
    else:
        root = child

    if return_format == "string":
        # pretty string
        s = etree.tostring(root, pretty_print=True)
        return s
    else:
        return root


def serialize_relation(model_relation, envelope=True, filter_nodes_ids=None, filter_way_ids = None, return_format="string"):
    """
    #from http://www.openstreetmap.org/relation/11 as example
    http://www.openstreetmap.org/api/0.6/relation/11
    <osm>
        <relation id="11" visible="true" version="31" changeset="19202376" timestamp="2013-11-30T22:53:08Z" user="will_p" uid="207845">
            <member type="way" ref="249285853" role="inner"/>
            <member type="way" ref="249285856" role="inner"/>
            <member type="way" ref="249285840" role="inner"/>
            <member type="way" ref="249285851" role="inner"/>
            <member type="way" ref="249285847" role="inner"/>
            <member type="way" ref="249285859" role="inner"/>
            <member type="way" ref="249285848" role="inner"/>
            <member type="way" ref="8125151" role="outer"/>
            <member type="way" ref="8125152" role="inner"/>
            <member type="way" ref="29502253" role="inner"/>
            <member type="way" ref="29694545" role="inner"/>
            <member type="way" ref="29694801" role="inner"/>
            <member type="way" ref="29694803" role="inner"/>
            <member type="way" ref="29694821" role="inner"/>
            <member type="way" ref="29694823" role="inner"/>
            <member type="way" ref="29694830" role="inner"/>
            <member type="way" ref="29694844" role="inner"/>
            <member type="way" ref="29872852" role="inner"/>
            <member type="way" ref="29873103" role="inner"/>
            <tag k="name" v="Tween Pond"/>
            <tag k="natural" v="water"/>
            <tag k="type" v="multipolygon"/>
        </relation>
    </osm>
    """


    # another child with text
    child = etree.Element('relation', id=str(model_relation.id), changeset=str(model_relation.changeset.id),
                          user=model_relation.changeset.created_by.username, uid=str(model_relation.changeset.created_by.id),
                          timestamp=model_relation.timestamp.isoformat() + "Z", visible="true", version="1")

    for model_tag in model_relation.tags.all():
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    qry_nodes = model_relation.nodes.all()
    if filter_nodes_ids:
        qry_nodes = qry_nodes.filter(pk__in=filter_nodes_ids)

    for model_node in qry_nodes:
        node_rel = RelationToNode.objects.filter(relation=model_relation, node=model_node)[0]
        node_child = etree.Element('member', type="node", ref=str(model_node.id), role=node_rel.role)
        child.append(node_child)

    qry_ways = model_relation.ways.all()
    if filter_way_ids:
        #only add ways that are in the list
        qry_ways = qry_ways.filter(pk__in=filter_way_ids)

    for model_way in qry_ways:
        way_rel = RelationToWay.objects.filter(relation=model_relation, way=model_way)[0]
        way_child = etree.Element('member', type="way", ref=str(model_way.id), role=way_rel.role)
        child.append(way_child)

    # create XML
    if envelope:
        root = etree.Element('osm')
        root.append(child)
    else:
        root = child

    if return_format == "string":
        # pretty string
        s = etree.tostring(root, pretty_print=True)
        return s
    else:
        return root


def serialize_map(bounds, changeset=None):
    # get the ways

    li_children = []
    # filter_node_ids = [nd.id for nd in nodes]
    # for node in nodes:
    #     xml_node = serialize_node(node, envelope=False, return_format="xml")
    #     li_children.append(xml_node)
    left, bottom, right, top = bounds
    poly = Polygon(((left, bottom), (left, top), (right, top), (right, bottom), (left, bottom)))


    # dct_way_ids = WayNodes.objects.filter(node__in=nodes).values('way_id').distinct()
    # li_way_ids = [x["way_id"] for x in dct_way_ids]
    # for way_id in li_way_ids:
    #     model_way = Way.objects.get(id=way_id)
    #     xml_way = serialize_way(model_way, envelope=False, filter_nodes_ids=None, return_format="xml")
    #     li_children.append(xml_way)
    li_way_ids = []

    model_changeset = None
    if changeset:
        try:
            model_changeset = Changeset.objects.get(id=changeset)
        except:
            pass

    qry_way = Way.objects.all()
    qry_node = Node.objects.all()


    qry_way = qry_way.filter(changeset=model_changeset)
    qry_node = qry_node.filter(changeset=model_changeset)

    for model_way in qry_way.filter(geom__bboverlaps=poly.wkt):
        xml_way = serialize_way(model_way, envelope=False, filter_nodes_ids=None, return_format="xml")
        li_children.append(xml_way)
        li_way_ids.append(model_way.id)

    #use distinct because the same way can belong to multiple relations
    for dct_relid in RelationToWay.objects.filter(way_id__in=li_way_ids).values('relation_id').distinct():
        model_rel = Relation.objects.get(id=dct_relid["relation_id"])
        xml_rel = serialize_relation(model_rel, envelope=False, filter_nodes_ids=None,
                                     filter_way_ids=li_way_ids, return_format="xml")
        li_children.append(xml_rel)

    root = etree.Element('osm')
    #append the bbox
    root.append(etree.Element("bounds", minlat=str(bounds[1]), minlon=str(bounds[0]), maxlat=str(bounds[3]), maxlon=str(bounds[2])))


    #get all the nodes that I need to show the ways and append to the root
    li_node_ids = []
    for dct_nodeid in WayNodes.objects.filter(way_id__in=li_way_ids).values('node_id').distinct():
        model_node = Node.objects.get(id=dct_nodeid["node_id"])
        xml_node = serialize_node(model_node, envelope=False, return_format="xml")
        if model_node.id not in li_node_ids:
            li_node_ids.append(model_node.id)
            #append all the nodes need by the ways
            root.append(xml_node)

    #get any additional nodes that aren't used in a way or relations
    nodes = qry_node.filter(geom__within=poly.wkt).exclude(id__in=li_node_ids)
    for node in nodes:
        xml_node = serialize_node(node, envelope=False, return_format="xml")
        root.append(xml_node)

    for child in li_children:
        root.append(child)

    s = etree.tostring(root, pretty_print=True)
    return s
