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

def serialize_node(model_node):
    """
    Given a model_node, return it per http://wiki.openstreetmap.org/wiki/API_v0.6#Response_12
    """
    lon, lat = model_node.geom.coords

    # create XML
    root = etree.Element('osm')
    # another child with text
    child = etree.Element('node', id=str(model_node.id), changeset=str(model_node.changeset.id), lat=str(lat), lon=str(lon),
                          timestamp=model_node.timestamp.isoformat(), visible="true", uid=str(model_node.changeset.created_by.id),
                          user=model_node.changeset.created_by.username)

    for model_tag in model_node.tags:
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    root.append(child)

    # pretty string
    s = etree.tostring(root, pretty_print=True)
    return s


def serialize_way(model_way):
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

    # create XML
    root = etree.Element('osm')
    # another child with text
    child = etree.Element('way', id=str(model_way.id), changeset=str(model_way.changeset.id),
                          user=model_way.changeset.created_by.username, uid=str(model_way.changeset.created_by.id),
                          timestamp=model_way.timestamp.isoformat(), visible="true")

    for model_tag in model_way.tags:
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    for node in model_way.nodes.all():
        node_child = etree.Element('nd', ref=str(node.id))
        child.append(node_child)
    root.append(child)

    # pretty string
    s = etree.tostring(root, pretty_print=True)
    return s


def serialize_relation(model_relation):
    """
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

    # create XML
    root = etree.Element('osm')
    # another child with text
    child = etree.Element('relation', id=str(model_relation.id), changeset=str(model_relation.changeset.id),
                          user=model_relation.changeset.created_by.username, uid=str(model_relation.changeset.created_by.id),
                          timestamp=model_relation.timestamp.isoformat(), visible="true")

    for model_tag in model_relation.tags:
        tag_child = etree.Element('tag', k=model_tag.key, v=model_tag.val)
        child.append(tag_child)

    for node_rel in RelationToNode.objects.filter(relation=model_relation):
        model_node = node_rel.node
        node_child = etree.Element('member', type="node", ref=str(model_node.id), role=node_rel.role)
        child.append(node_child)

    for way_rel in RelationToWay.objects.filter(relation=model_relation):
        model_way = way_rel.way
        way_child = etree.Element('member', type="way", ref=str(model_way.id), role=way_rel.role)
        child.append(way_child)

    root.append(child)

    # pretty string
    s = etree.tostring(root, pretty_print=True)
    return s
