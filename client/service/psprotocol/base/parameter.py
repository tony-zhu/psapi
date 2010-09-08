"""An object representation of "Parameter" in perfSONAR protocol.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject

class Parameter(PsObject):
    """An object representation of "Parameter" in perfSONAR protocol.
    """
    
    def __init__(self, name, value=None, nested=None):
        if not (value or nested):
            # TODO: raise an exception at least one value must be defined
            pass
        self.name = name
        self.value = value
        self.nested = nested
        self._check_values()
    
        
    def _check_values(self):
        
        if isinstance(self.nested, PsObject):
            self.nested = [self.nested]
        elif isinstance(self.nested, list):
            for c in self.nested:
                if not isinstance(c, PsObject):
                    # TODO: raise an exception
        
                    pass
        elif isinstance(self.nested, str):
            pass
        else:
            # TODO raise an exception
            pass
        
        return True
        
                
    def serialize(self, root=None, tostring=True):
    
        self._check_values()
        
        if root is not None:
            param = etree.SubElement(root, '{%s}parameter' % ns.NMWG)
        else:
            param = etree.Element('{%s}parameter' % ns.NMWG, nsmap = ns.nsmap)
        
        param.set('name', self.name)
        if self.value is not None:
            param.set('value', str(self.value))
            
        if self.nested:
            if isinstance(self.nested, str):
                param.text = self.nested
            elif isinstance(self.nested, PsObject):
                self.nested.serialize(param, tostring=False)
            elif isinstance(self.nested, list):
                for n in self.nested:
                    n.serialize(param, tostring=False)
            else:
                # TODO raise an exception
                pass
        
        if tostring:
            return etree.tostring(param, pretty_print=True)
        else:
            return param
    
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.fromstring(xml)
        return Parameter.parse_xml_tree(t)
    
    
    @staticmethod    
    def parse_xml_tree(tree):
        if tree.tag != "{%s}parameter" % ns.NMWG:
            # TODO raise exception
            pass
        name = tree.attrib['name']
        value = tree.attrib['value']
        
        # TODO: parameter child can be an element not only text
        text = tree.text
        
        return Parameter(name, value, text)
        
