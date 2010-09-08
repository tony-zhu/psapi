"""Create PsObject(s) from XML string or stream.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree


def parse_xml_tree(tree):
    # The imports are here to avoid cyclic depandencies
    from psapi.client.service import namespaces as ns
    from psapi.client.service.psprotocol.base import Message
    from psapi.client.service.psprotocol.base import Parameter
    from psapi.client.service.psprotocol.base import Parameters
    from psapi.client.service.psprotocol.base import Metadata
    from psapi.client.service.psprotocol.base import Data
    from psapi.client.service.psprotocol.base import Subject
    
    if tree.tag == "{%s}message" % ns.NMWG:
        return Message.parse_xml_tree(tree)
    elif tree.tag == "{%s}parameters" % ns.NMWG:
        return Parameters.parse_xml_tree(tree)
    elif tree.tag == "{%s}parameter" % ns.NMWG:
        return Parameter.parse_xml_tree(tree)
    elif tree.tag == "{%s}metadata" % ns.NMWG:
        return Metadata.parse_xml_tree(tree)
    elif tree.tag == "{%s}data" % ns.NMWG:
        return Data.parse_xml_tree(tree)
    elif tree.tag == "{%s}subject" % ns.NMWG:
        return Subject.parse_xml_tree(tree)
        
def parse_xml_string(xml):
    """
    """
    t = etree.fromstring(xml)
    return parse_xml_tree(t)
    
