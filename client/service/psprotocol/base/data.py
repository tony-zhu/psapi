"""An object representation of "Data" in perfSONAR protocol.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Metadata

class Data(PsObject):
    """An object representation of "Data" in perfSONAR protocol.
    """
    
    def __init__(self, children, idref=None, id=None):
        """The child element can be any element of type PsObject.
        
        Each data element must reference a metadata element, hence the idref
        here is required.
        idref can be a metadata object or a string.
        """
        self.children = children
        self.id = id
        self.idref = idref
        self._check_values()
    
        
    def _check_values(self):
        """Auxiliary method to validate value types.
        """
        
        if id is None:
            self.id =  "data.%i" % self._generate_id()
        
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
            data = etree.SubElement(root, '{%s}data' % ns.NMWG)
        else:
            data = etree.Element('{%s}data' % ns.NMWG, nsmap = ns.nsmap)
        
        data.set('id', self.id)
        if self.idref:
            data.set('metadataIdRef', self.idref)
        
        if isinstance(self.idref, Metadata):
            data.set('metadataIdRef', self.idref.id)
        else:
            data.set('metadataIdRef', self.idref)
            
        for c in self.children:
            c.serialize(data, tostring=False)
        
        if tostring:        
            return etree.tostring(data, pretty_print=True)
        else:
            return data
        
        
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.fromstring(xml)
        return Data.parse_xml_tree(t)
    
    
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
        
        return Data(obj, id, idref)
