__author__ = 'micah'

from lxml import etree
from models import RelationToWay, RelationToNode


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
                          timestamp=model_node.timestamp.isoformat(), visible="true", uid=str(model_node.changeset.created_by.id),
                          user=model_node.changeset.created_by.username)

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
                          timestamp=model_way.timestamp.isoformat(), visible="true")

    for model_tag in model_way.tags.all():
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    qry_nodes = model_way.nodes.all()
    if filter_nodes_ids:
        qry_nodes = qry_nodes.filter(pk__in=filter_nodes_ids)
    for node in qry_nodes:
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


def serialize_relation(model_relation, envelope=True, filter_nodes_ids=None, return_format="string"):
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
                          timestamp=model_relation.timestamp.isoformat(), visible="true")

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


    li_ways = []
    qry_ways = model_relation.ways.all()
    if filter_nodes_ids:
        #only add ways with a node in the list
        for check_way in qry_ways:
            if check_way.nodes.filter(pk__in=filter_nodes_ids):
                li_ways.append(check_way)
    else:
        li_ways = list(qry_ways)

    for model_way in li_ways:
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


def serialize_map(bounds, nodes):
    # get the ways
    li_children = [etree.Element("bounds", minlat=bounds[1], minlon=bounds[0], maxlat=bounds[3], maxlon=bounds[2]),]
    filter_node_ids = [nd.id for nd in nodes]
    for node in nodes:
        xml_node = serialize_node(node, envelope=False, return_format="xml")
        li_children.append(xml_node)
        for way in node.way_set.all():
            xml_way = serialize_way(way, envelope=False, filter_nodes_ids=filter_node_ids, return_format="xml")
            li_children.append(xml_way)
        for relation in node.relation_set.all():
            xml_rel = serialize_way(relation, envelope=False, filter_nodes_ids=filter_node_ids, return_format="xml")
            li_children.append(xml_rel)




