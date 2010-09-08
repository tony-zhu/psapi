"""An object representation of "Parameters" in perfSONAR protocol.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Parameter

class Parameters(PsObject):
    """An object representation of "Parameters" in perfSONAR protocol.
    
    This object also implements dictionary like interface to iterate over the
    different parameters.
    """
    
    def __init__(self, parameters, id=None):
        self.id = id
        self.parameters = parameters
        self._check_values()
    
        
    def _check_values(self):
        if self.id is None:
            self.id = "parameters.%i" % self._generate_id()
        
        params = {}    
        if isinstance(self.parameters, PsObject):
            params = {self.parameters.name: self.parameters}
        elif isinstance(self.parameters, dict):
            for p in self.parameters:
                if not isinstance(p, PsObject):
                    # TODO: raise an exception
                    pass
            params = self.parameters
        elif isinstance(self.parameters, list):
            for p in self.parameters:
                if isinstance(p, PsObject):
                    params[p.name] = p
                else:
                    # TODO: raise an exception
                    pass
        else:
            # TODO raise an exception
            pass
        self.parameters = params
        return True
        
                
    def serialize(self, root=None, tostring=True):
    
        self._check_values()
        
        if root is not None:
            params = etree.SubElement(root, '{%s}parameters' % ns.NMWG)
        else:
            params = etree.Element('{%s}parameters' % ns.NMWG, nsmap = ns.nsmap)
        
        params.set('id', self.id)
        
        for p in self.parameters:
            self.parameters[p].serialize(root=params, tostring=False)
        
        if tostring:
            return etree.tostring(params, pretty_print=True)
        else:
            return params
    
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.fromstring(xml)
        return Parameters.parse_xml_tree(t)
    
    
    @staticmethod    
    def parse_xml_tree(tree):
        if tree.tag != "{%s}parameters" % ns.NMWG:
            # TODO raise exception
            pass
        id = tree.attrib['id']
        
        pp = tree.findall("{%s}parameter" % ns.NMWG)
        params = {}
        for p in pp:
            tmp = Parameter.parse_xml_tree(p)
            params[tmp.name] = tmp
        
        return Parameters(params, id)
        
