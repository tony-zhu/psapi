"""An object representation of "subject" in perfSONAR protocol.
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject

class Subject(PsObject):
    """An object representation of "subject" in perfSONAR protocol.
    """
    
    def __init__(self, children, id=None, idref=None):
        self.children = children
        self.id = id
        self.idref = idref
        
        self._check_values()
    
    
    def _check_values(self):
        if self.id is None:
            self.id = "subject.%i" % self._generate_id()
            
        if isinstance(self.children, PsObject):
            self.children = [self.children]
        elif isinstance(self.children, list):
            for c in self.children:
                if not isinstance(c, PsObject):
                    # TODO: raise an exception
                    pass
        else:
            # TODO raise an exception
            pass
        
        return True
    
    
    def serialize(self, root=None, tostring=True):
        
        self._check_values()
        
        if root is not None:
            subject = etree.SubElement(root, '{%s}subject' % ns.NMWG)
        else:
            subject = etree.Element('{%s}subject' % ns.NMWG, nsmap = ns.nsmap)
        
        subject.set('id', self.id)
        if self.idref:
            subject.set('metadataIdRef', self.idref)
            
        for c in self.children:
            c.serialize(root=subject, tostring=False)
        
        if tostring:
            return etree.tostring(subject, pretty_print=True)
        else:
            return subject
    
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.parse(xml)
        parse_xml_tree(t)
    
    
    @staticmethod    
    def parse_xml_tree(tree):
        if tree.tag != "{%s}subject" % ns.NMWG:
            # TODO raise exception
            pass
        id = tree.attrib['idref']
        idref = None
        if 'metadataIdRef' in tree.attrib:
            idref = tree.attrib['metadataIdRef']
        
        # TODO parse children
        children = PsObject()
        
        return Subject(children, id, idref)
        
