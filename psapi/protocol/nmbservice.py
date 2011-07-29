#!/usr/bin/env python

"""NM Base Service representation."""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


import re
from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns


class NMBService(PsObject):
    """See nmb:service schema."""
    def __init__(self, name=None, type=None, address=None, address_type=None, \
                 description=None, object_id=None):
        PsObject.__init__(self, object_id, None)
        self.name = name
        self.type = type
        self.address = address
        self.address_type = address_type
        self.description = description

    def __eq__(self, other):
        if not isinstance(self, other):
            return False

        attrs = ['object_id', 'name', 'type',  'address', 'address_type', \
                 'description']

        for attr in attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}service' % ns.NMB)
        children = {'name': None, 'type': None, 'address': None, \
                    'address_type': None, 'description': None}

        for child in tree.iterchildren():
            groups = re.match("{(.*)}(.*)", child.tag).groups()
            if groups[0] == ns.NMB and groups[1] in children:
                children[groups[1]] = child.text
                if groups[1] == 'address':
                    children['address_type'] = child.get('type', None)

        children['object_id'] = tree.get('id')
        return NMBService(**children)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}service' % ns.NMB, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}service' % ns.NMB)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        attrs = {'name': None, 'type': None, \
                    'address': None, 'description': None}

        for attr in attrs:
            child = etree.SubElement(tree, '{%s}%s' % (ns.NMB, attr))
            child.text = getattr(self, attr)
            if attr == 'address' and getattr(self, 'address_type') is not None:
                child.set('type', getattr(self, 'address_type'))

        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
