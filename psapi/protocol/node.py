#!/usr/bin/env python

"""
Topology Node type
Node = 
        element nmwgtopo3:node {
                NodeContent
        }

NodeContent =
        Identifier? &
        BaseNodeIdRef? &
        BaseRole? &
        BaseName? &        
        element nmwgtopo3:type { xsd:string }? &
        element nmwgtopo3:hostName { xsd:string }? &
        element nmwgtopo3:description { xsd:string }? &
        element nmwgtopo3:cpu { xsd:string }? &
        element nmwgtopo3:operSys { xsd:string }? &
        element nmwgtopo3:location {
                LocationContent
        }? &
        element nmwgtopo3:institution { xsd:string }? &        
        element nmwgtopo3:country { xsd:string }? &
        element nmwgtopo3:city { xsd:string }? &                
        element nmwgtopo3:latitude { xsd:float }? &
        element nmwgtopo3:longitude { xsd:float }? &                
        (
                BaseInterface |
                L2Interface |
                L3Interface
        )*

"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import re
from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns

from psapi.utils.ipaddress import get_address_type


class Node(PsObject):
    """See nmwgt:interface schema."""
    def __init__(self, name=None, hostName=None, description=None, \
                  cpu=None, operSys=None, object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.name = name
        self.hostName = hostName
        self.description = description
        self.cpu = cpu
        self.operSys = operSys
       

    def __eq__(self, other):
        attrs = ['name', 'hostName', 'description', 'cpu', 'operSys']
        for attr in attrs:
            if hasattr(self, attr) and not hasattr(other, attr):
                return False
            if not hasattr(self, attr) and hasattr(other, attr):
                return False
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}node' % ns.NMWGTOPO3)
        children = {}
        children['name'] = None
        children['hostName'] = None
        children['description'] = None
        children['cpu'] = None
        children['operSys'] = None
        

        for child in tree.iterchildren():
            groups = re.match("{(.*)}(.*)", child.tag).groups()
            if groups[0] == ns.NMWGTOPO3 and groups[1] in children:
                if child.text is None:
                    # A special case for Address elements
                    children[groups[1]] = child.get('value')
                else:
                    children[groups[1]] = child.text

        return Node(**children)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}node' % ns.NMWGTOPO3, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}node' % ns.NMWGTOPO3)

        attrs = ['name', 'hostName', 'description', 'cpu', 'operSys']

        for attr in attrs:
            if getattr(self, attr) is not None:
                node = etree.SubElement(tree, '{%s}%s' % (ns.NMWGTOPO3, attr))
                node.text = str(getattr(self, attr))

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
