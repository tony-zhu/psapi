"""An object representation of "Metadata" in perfSONAR protocol.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject

class Metadata(PsObject):
    """An object representation of "Metadata" in perfSONAR protocol.
    """

    def __init__(self, children, id=None, idref=None):
        """The child element can be any element of type PsObject.
        """
        self.children = children
        self.id = id
        self.idref = idref
        self._check_values()

    def _check_values(self):
        """Auxiliary method to validate value types.
        """
        if id is None:
            self.id =  "metadata.%i" % self._generate_id()
        
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
            meta = etree.SubElement(root, '{%s}metadata' % ns.NMWG)
        else:
            meta = etree.Element('{%s}metadata' % ns.NMWG, nsmap = ns.nsmap)
        
        meta.set('id', self.id)
        if self.idref:
            meta.set('metadataIdRef', self.idref)
            
        for c in self.children:
            c.serialize(meta)
        
        if tostring:        
            return etree.tostring(meta, pretty_print=True)
        else:
            return meta
    
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.fromstring(xml)
        return Metadata.parse_xml_tree(t)
    
        
    @staticmethod    
    def parse_xml_tree(tree):
        if tree.tag != "{%s}message" % ns.NMWG:
            # TODO raise exception
            pass
        id = tree.attrib['id']
        idref = None
        if 'metadataIdRef' in tree.attrib:
            idref = tree.attrib['metadataIdRef']
        
        # TODO parse children
        obj = PsObject()
        
        return Metadata(obj, id, idref)
        
