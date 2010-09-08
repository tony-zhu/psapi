"""An object representation of "Message" in perfSONAR protocol.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import parse_xml_tree

from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Parameter
from psapi.client.service.psprotocol.base import Parameters
from psapi.client.service.psprotocol.base import Metadata
from psapi.client.service.psprotocol.base import Data

class Message(PsObject):
    """An object representation of "Message" in perfSONAR protocol.
    """
    
    def __init__(self, type, metadata, data=None, parameters=None,
                id=None, idref=None):
        """
        While the protocol specification require each message to have Data
        section, by the specification the Data section can be empty. If the user
        didn't specify a Data section, the default empty Data will be used.
        
        keyword arguments
        type -- request, response
        metadata -- list of one or more metadata objects
        data -- a list of zero or more data objects
        parameters -- a list of zero or more parameter objects
        id -- a message id, if not supplied an unique message id will be generated
        refid -- a message reference id from previous messages
        
        """
        self.type = type
        self.metadata = metadata
        self.data = data
        self.parameters = parameters    
        self.idref = idref
        self.id = id
        
        self._check_values()
    
    def _check_values(self):
        """Auxiliary method to validate value types.
        """
        
        if self.type is None:
            # TODO raise an exception
            pass
            
        if self.id is None:
            self.id = "messsage.%i" % self._generate_id()
        
        if isinstance(self.metadata, list):
            if len(self.metadata) == 0:
                # TODO raise an exception
                pass
                
            for m in self.metadata:
                if not isinstance(m, Metadata):
                    # TODO raise an exception
                    pass
        elif isinstance(self.metadata, Metadata):
            self.metadata = [self.metadata]
        else:
            # TODO raise an exception
            pass
        
        if isinstance(self.data, list):
            for d in self.data:
                if not isinstance(d, Data):
                    # TODO raise an exception
                    pass
        elif isinstance(self.data, Data):
            self.data = [self.Data]
        elif self.data is None:
            # TODO: do we need an exception or generate empty data elements?
            self.data = []
        else:
            # TODO raise an exception
            pass
                
        if isinstance(self.parameters, list):
            self.parameters = Parameters(self.parameters)
        elif isinstance(self.parameters, Parameter):
            self.parameters = Parameters(self.parameters)
        elif isinstance(self.parameters, Parameters):
            pass
        elif self.parameters is None:
            pass
        else:
            # TODO raise an exception
            pass
            
        self._check_metadata_data_ref()
        return True
        
    def _check_metadata_data_ref(self):
        """Makes  sure that each metadata element has a data element.
        """
        # TODO check that each metadata object has a corresponding data object.
        pass
        
    def serialize(self, root=None, tostring=True):
        """Serialize the message object to XML representation.
        
        Note an XML generator can be used, but this case is not complicated!
        """
        self._check_values()
        
        m = etree.Element('{%s}message' % ns.NMWG, nsmap = ns.nsmap)
        m.set('type', self.type)
        m.set('id', self.id)
        if self.idref:
            m.set('metadataIdRef', self.idref)
        
        for meta in self.metadata:
            meta.serialize(m)
        
        for d in self.data:
            d.serialize(m)
                    
        if self.parameters is not None:
                self.parameters.serialize(m)
                
        if tostring:        
            return etree.tostring(m, pretty_print=True)
        else:
            return m
    
    @staticmethod        
    def parse_xml_tree(tree):
        if tree.tag != "{%s}message" % ns.NMWG:
            # TODO raise exception
            pass
        
        type = tree.attrib['type']
        id = tree.attrib['id']
        idref = None
        if 'messageIdRef' in tree.attrib:
            idref = tree.attrib['messageIdRef']
        
        
        meta = []
        data = []
        parameters = None
                
        for c in tree.getchildren():
            obj = parse_xml_tree(c)
            
            if isinstance(obj, Metadata):
                meta.append(obj)
            elif isinstance(obj, Data):
                data.append(obj)
            elif isinstance(obj, Parameters):
                parameters= obj
            else:
                # TODO raise an exception
                pass
 
        return Message(type, meta, data, parameters, id, idref)
    
    
    
    @staticmethod    
    def parse_xml(xml):
        t = etree.fromstring(xml)
        return Message.parse_xml_tree(t)
