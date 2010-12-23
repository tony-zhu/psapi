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
                  object_id=None, ref_id=None):
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

    def __eq__(self, other):
        attrs = ['direction', 'ifType', 'ifHostName', 'hostName', \
                    'ifDescription', 'classofService', 'ifIndex', \
                    'capacity', 'ifName', 'ipAddress', 'authRealm', \
                    'ifAddress']
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
        if isinstance(xml, str):
            tree = etree.fromstring(xml)
        else:
            tree = xml
        
        if tree.tag != '{%s}interface' % ns.NMWGT:
            raise Exception("Found element of type '%s' while expecting\
             element of type '%s'" % \
             (tree.tag, '{%s}interface' % ns.NMWGT))
        
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
            tree = etree.Element('{%s}interface' % ns.NMWGT, nsmap = ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}interface' % ns.NMWGT)
        
        if self.ipAddress is not None:
            ip = etree.SubElement(tree, '{%s}ipAddress' % ns.NMWGT)
            print "ip: ", self.ipAddress
            ip.text = self.ipAddress
            ip.set('type', get_address_type(self.ipAddress))
        
        if self.hostName is not None:
            hostName = etree.SubElement(tree, '{%s}hostName' % ns.NMWGT)
            hostName.text = self.hostName
        
        if self.ifName is not None:
            ifName = etree.SubElement(tree, '{%s}ifName' % ns.NMWGT)
            ifName.text = self.ifName
        
        if self.ifDescription is not None:
            ifDescription = etree.SubElement(tree, '{%s}ifDescription' % ns.NMWGT)
            ifDescription.text = self.ifDescription
        
        if self.ifAddress is not None:
            ifAddress = etree.SubElement(tree, '{%s}ifAddress' % ns.NMWGT)
            ifAddress.text = self.ifAddress
            ifAddress.set('type', get_address_type(self.ifAddress))
        
        if self.ifHostName is not None:
            ifHostName = etree.SubElement(tree, '{%s}ifHostName' % ns.NMWGT)
            ifHostName.text = self.ifAddress
        
        if self.ifIndex is not None:
            ifIndex = etree.SubElement(tree, '{%s}ifIndex' % ns.NMWGT)
            ifIndex.text = self.ifIndex
        
        if self.ifType is not None:
            ifType = etree.SubElement(tree, '{%s}ifType' % ns.NMWGT)
            ifType.text = self.ifType
        
        if self.direction is not None:
            direction = etree.SubElement(tree, '{%s}direction' % ns.NMWGT)
            direction.text = self.direction
        
        if self.authRealm is not None:
            authRealm = etree.SubElement(tree, '{%s}authRealm' % ns.NMWGT)
            authRealm.text = self.authRealm
        
        if self.classofService is not None:
            classofService = etree.SubElement(tree, '{%s}classofService' % ns.NMWGT)
            classofService.text = self.classofService
        
        if self.capacity is not None:
            capacity = etree.SubElement(tree, '{%s}capacity' % ns.NMWGT)
            capacity.text = self.capacity
        
        if tostring:        
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
