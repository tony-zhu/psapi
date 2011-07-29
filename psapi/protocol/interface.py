#!/usr/bin/env python

"""
Topology Interface type

InterfaceContent =
        element nmwgtopo:ipAddress {
                Address
        }? &
        element nmwgtopo:hostName { xsd:string }? &
        element nmwgtopo:ifName { xsd:string }? &
        element nmwgtopo:ifDescription { xsd:string }? &
        element nmwgtopo:ifAddress {
                Address
        }? &
        element nmwgtopo:ifHostName { xsd:string }? &
        element nmwgtopo:ifIndex { xsd:string }? &
        element nmwgtopo:type { xsd:string }? &
        element nmwgtopo:direction { xsd:string }? &
        element nmwgtopo:authRealm { xsd:string }? &
        element nmwgtopo:classOfService { xsd:string }? &
        element nmwgtopo:capacity { xsd:string }?

Address =
        (
                attribute value { xsd:string } |
                text
        ) &
        attribute type { xsd:string }
    
    
    Note:
        Some SNMPMA uses description instead of ifDescription
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import re
from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns

from psapi.utils.ipaddress import get_address_type


class Interface(PsObject):
    """See nmwgt:interface schema."""
    def __init__(self, ipAddress=None, hostName=None, ifName=None, \
                  ifDescription=None, ifAddress=None, ifHostName=None, \
                  ifIndex=None, ifType=None, direction=None, \
                  authRealm=None, classofService=None, capacity=None, \
                  description=None, object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.ipAddress = ipAddress
        self.hostName = hostName
        self.ifName = ifName
        self.ifDescription = ifDescription
        self.ifAddress = ifAddress
        self.ifHostName = ifHostName
        self.ifIndex = ifIndex
        self.ifType = ifType
        self.direction = direction
        self.authRealm = authRealm
        self.classofService = classofService
        self.capacity = capacity
        self.description = description

    def __eq__(self, other):
        attrs = ['direction', 'ifType', 'ifHostName', 'hostName', \
                    'ifDescription', 'classofService', 'ifIndex', \
                    'capacity', 'ifName', 'ipAddress', 'authRealm', \
                    'ifAddress', 'description']
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
        tree = PsObject.assert_xml(xml, '{%s}interface' % ns.NMWGT)
        children = {}
        children['ipAddress'] = None
        children['hostName'] = None
        children['ifName'] = None
        children['ifDescription'] = None
        children['ifAddress'] = None
        children['ifHostName'] = None
        children['ifIndex'] = None
        children['ifType'] = None
        children['direction'] = None
        children['authRealm'] = None
        children['classofService'] = None
        children['capacity'] = None
        children['description'] = None

        for child in tree.iterchildren():
            groups = re.match("{(.*)}(.*)", child.tag).groups()
            if groups[0] == ns.NMWGT and groups[1] in children:
                if child.text is None:
                    # A special case for Address elements
                    children[groups[1]] = child.get('value')
                else:
                    children[groups[1]] = child.text

        return Interface(**children)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}interface' % ns.NMWGT, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}interface' % ns.NMWGT)

        if self.ipAddress:
            if hasattr(self.ipAddress, 'to_xml'):
                self.ipAddress.to_xml(tree)
            else:
                ip = etree.SubElement(tree, '{%s}ipAddress' % ns.NMWGT)
                ip.text = self.ipAddress
                ip.set('type', get_address_type(self.ipAddress))

        if self.ifAddress:
            if hasattr(self.ifAddress, 'to_xml'):
                self.ifAddress.to_xml(tree)
            else:
                ifAddress = etree.SubElement(tree, '{%s}ifAddress' % ns.NMWGT)
                ifAddress.text = self.ifAddress
                # ifAddress.set('type', get_address_type(self.ifAddress))

        attrs = ['direction', 'ifType', 'ifHostName', 'hostName', \
                    'ifDescription', 'classofService', 'ifIndex', \
                    'capacity', 'ifName', 'authRealm', 'description']

        for attr in attrs:
            if getattr(self, attr) is not None:
                node = etree.SubElement(tree, '{%s}%s' % (ns.NMWGT, attr))
                node.text = str(getattr(self, attr))

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
