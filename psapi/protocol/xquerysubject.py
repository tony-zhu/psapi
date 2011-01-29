#!/usr/bin/env python
"""
XQuery Subject
"""
__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Subject
from psapi.protocol import namespaces as ns


class XQuerySubject(Subject):
    """See xquery:subject schema."""
    def __init__(self, query=None, object_id=None):
        Subject.__init__(self, query, object_id, None)

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}subject' % ns.XQUERY)
        object_id = tree.get('id')
        query = tree.text

        return XQuerySubject(query, object_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}subject' % ns.XQUERY, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}subject' % ns.XQUERY)

        if self.object_id is not None:
            tree.set('id', self.object_id)

        if self.contents is not None:
            tree.text = self.contents

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
