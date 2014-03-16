__author__ = 'micah'

from lxml import etree

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

    for node in model_way.nodes.all():
        node_child = etree.Element('nd', ref=str(node.id))
        child.append(node_child)
    root.append(child)

    # pretty string
    s = etree.tostring(root, pretty_print=True)
    return s
