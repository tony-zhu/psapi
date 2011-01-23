#!/usr/bin/env python

"""PS Service representation."""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import re
from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns


class PsService(PsObject):
    """See psservice:service schema."""
    def __init__(self, serviceName=None, accessPoint=None, \
                    serviceType=None, serviceDescription=None, object_id=None):
        PsObject.__init__(self, object_id, None)
        self.serviceName = serviceName
        self.accessPoint = accessPoint
        self.serviceType = serviceType
        self.serviceDescription = serviceDescription

    def __eq__(self, other):
        if not isinstance(self, other):
            return False

        attrs = ['object_id', 'serviceName', 'accessPoint', \
                    'serviceType', 'serviceDescription']

        for attr in attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}service' % ns.PSSERVICE)
        children = {'serviceName': None, 'accessPoint': None, \
                    'serviceType': None, 'serviceDescription': None}

        for child in tree.iterchildren():
            groups = re.match("{(.*)}(.*)", child.tag).groups()
            if groups[0] == ns.PSSERVICE and groups[1] in children:
                children[groups[1]] = child.text

        children['object_id'] = tree.get('id')
        return PsService(**children)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}service' % \
                                        ns.PSSERVICE, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}service' % ns.PSSERVICE)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        attrs = {'serviceName': None, 'accessPoint': None, \
                    'serviceType': None, 'serviceDescription': None}

        for attr in attrs:
            child = etree.SubElement(tree, '{%s}%s' % (ns.PSSERVICE, attr))
            child.text = getattr(self, attr)

        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
