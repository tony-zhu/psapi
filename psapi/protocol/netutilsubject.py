#!/usr/bin/env python
"""
Specific SNMP Subject that takes only Interface as a content.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns
from psapi.protocol.xmlmapper import parse_psobject_from_xml


class NetUtilSubject(Subject):
    """See netutil:subject schema."""
    def __init__(self, interface=None, object_id=None, ref_id=None):
        Subject.__init__(self, interface, object_id, ref_id)    
    
    @staticmethod
    def from_xml(xml):
        if isinstance(xml, str):
            tree = etree.fromstring(xml)
        else:
            tree = xml
        
        if tree.tag != '{%s}subject' % ns.NETUTIL:
            raise Exception("Found element of type '%s' while expecting\
                            element of type '%s'" % \
                            (tree.tag, '{%s}subject' % ns.NETUTIL))
        
        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')
        
        contents = []
        
        for cont in tree.iterchildren():
            contents.append(parse_psobject_from_xml(cont))
        
        if len(contents) == 0:
            contents = None
        elif len(contents) == 1:
            contents = contents[0]
        
        return NetUtilSubject(contents, object_id, ref_id)
    
    
    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}subject' % ns.NETUTIL, nsmap = ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}subject' % ns.NETUTIL)
        
        if self.object_id is None:
            self.object_id = PsObject.generate_id()
        
        tree.set('id', self.object_id)
        
        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)
        
        if self.contents is None:
            pass 
        elif isinstance(self.contents, PsObject):
            self.contents.to_xml(tree, False)
        elif isinstance(self.contents, list):
            for cont in self.contents:
                if isinstance(cont, PsObject):
                    cont.to_xml(tree, False)
        
        if tostring:        
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
