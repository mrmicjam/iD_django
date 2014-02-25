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
    child = etree.Element('node', id=str(model_node.id), changeset="1", lat=str(lat), lon=str(lon),
                          timestamp=model_node.timestamp.isoformat(), visible="true", uid=str(model_node.id),
                          user=model_node.changeset.created_by.username)
    root.append(child)

    # pretty string
    s = etree.tostring(root, pretty_print=True)
    return s