#!/usr/bin/env python

"""EndPointPair representation.

Example:
<nmwgt:endPointPair xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/">
  <nmwgt:src type="ipv4">128.128.128.128</nmwgt:src>
  <nmwgt:dst type="hostname">dst.dst.com</nmwgt:dst>
</nmwgt:endPointPair>
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns

from psapi.utils.ipaddress import is_valid_ipv4
from psapi.utils.ipaddress import is_valid_ipv6

class EndPointPair(PsObject):
    """See nmwgt:endPointPair schema."""
    def __init__(self, src=None, dst=None, object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.src = src
        self.dst = dst
        
        if src is None:
            self.src_type = None
        elif is_valid_ipv4(src):
            self.src_type = 'ipv4'
        elif is_valid_ipv6(src):
            self.src_type = 'ipv6'
        else:
            self.src_type = 'hostname'
        
        if dst is None:
            self.dst_type = None
        elif is_valid_ipv4(dst):
            self.dst_type = 'ipv4'
        elif is_valid_ipv6(dst):
            self.dst_type = 'ipv6'
        else:
            self.dst_type = 'hostname'
    
    def __eq__(self, other):
        if self.src == other.src and self.dst == other.dst:
            return True
        else:
            return False
    def __ne__(self, other):
        return not self.__eq__(other)
    
    @staticmethod
    def from_xml(xml):
        if isinstance(xml, str):
            tree = etree.fromstring(xml)
        else:
            tree = xml
        
        if tree.tag != '{%s}endPointPair' % ns.NMWGT:
            raise Exception("Found element of type '%s' while expecting\
                        element of type '%s'" % \
                        (tree.tag, '{%s}endPointPair' % ns.NMWGT))
        
        src = None
        dst = None
        
        for child in tree.iterchildren():
            if child.tag == '{%s}src' % ns.NMWGT:
                if child.text is None:
                    src = child.get('value')
                else:
                    src = child.text
            elif child.tag == '{%s}dst' % ns.NMWGT:
                if child.text is None:
                    dst = child.get('value')
                else:
                    dst = child.text
            else:
                pass
        
        return EndPointPair(src, dst)
    
    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}endPointPair' % \
                                            ns.NMWGT, nsmap = ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}endPointPair' % ns.NMWGT)
        
        if self.src is not None:
            src = etree.SubElement(tree, '{%s}src' % ns.NMWGT)
            src.set('type', self.src_type)
            src.set('value', self.src)
        
        if self.dst is not None:
            dst = etree.SubElement(tree, '{%s}dst' % ns.NMWGT)
            dst.set('type', self.dst_type)
            dst.set('value', self.dst)
        
        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
