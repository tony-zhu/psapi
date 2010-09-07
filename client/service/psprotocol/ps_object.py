"""
An abstract object representation all elements in perfSONAR protocol.

Mainly, this is used to make sure that all children implements "serialize" and
"deserialize" methods.

For more into see: An extensible protocol for network measurement and control.
Open grid forum working group -- J Zurawski, M Swany 
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

class PsObject(object):
    """An abstract object representation all elements in perfSONAR protocol.
    """
    
    def __init__(self):
        pass
        
    def _generate_id(self):
        """Generate a unique id to be used as id attribute for different PsObjects.
        """
        global __LAST_PSOBJECT_ID__
        try:
            __LAST_PSOBJECT_ID__
        except NameError:
            __LAST_PSOBJECT_ID__ = 0
        
        __LAST_PSOBJECT_ID__ += 1
        return __LAST_PSOBJECT_ID__
        
    def serialize(self, root=None, tostring=True):
        """Serialize the object into XML that perfSONAR understands.
        
        If tostring is false an object of etree will be return. This case is
        useful for nested serialization where the user is not interested of the
        actual XML text.
        """
        pass
        
    @staticmethod    
    def parse_xml(xml):
        """Takes XML string as an input to create a Ps object.
        """
        t = etree.fromstring(xml)
        return PsObject.parse_xml_tree(t)
        
    @staticmethod    
    def parse_xml_tree(tree):
        """This is helpful for nested parsing of objects.
        """
        pass
        
    def __eq__(self, other):
        """Override the default equality to test to test the actual values of
        the class's attributes.
        """
        if not len(self.__dict__) ==  len(other.__dict__):
            return False
        for key in self.__dict__:
            if not key in other.__dict__:
                return False
            if not self.__dict__[key] == other.__dict__[key]:
                return False
        return True
