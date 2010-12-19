#!/usr/bin/env python

"""
Special Subject type for select filter
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns


class SelectSubject(Subject):
    """See select:subject schema."""
    def __init__(self, object_id=None, ref_id=None):
        Subject.__init__(self, None, object_id, ref_id)    
    
    @staticmethod
    def from_xml(xml):
        if isinstance(xml, str):
            tree = etree.fromstring(xml)
        else:
            tree = xml
        
        if tree.tag != '{%s}subject' % ns.SELECT:
            raise Exception("Found element of type '%s' while expecting\
                            element of type '%s'" % \
                            (tree.tag, '{%s}subject' % ns.SELECT))
        
        object_id = tree.get('id')
        ref_id = tree.get('metadataIdRef')
        
        return SelectSubject(object_id, ref_id)
    
    
    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}subject' % ns.SELECT, nsmap = ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}subject' % ns.SELECT)
        
        if self.object_id is None:
            self.object_id = PsObject.generate_id()
        
        tree.set('id', self.object_id)
        
        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)
        
        if tostring:        
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
