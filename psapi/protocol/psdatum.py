#!/usr/bin/env python

"""PS Service Datum representation."""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]


from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns


class PsDatum(PsObject):
    """See psservice:datum schema."""
    def __init__(self, contents=None, datum_type=None):
        PsObject.__init__(self, None, None)
        self.contents = contents
        self.datum_type = datum_type

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}datum' % ns.PSSERVICE)
        datum_type = tree.get('type')
        contents = []

        for child in tree.iterchildren():
            contents.append(PsObject.from_xml(child))

        return PsDatum(contents, datum_type)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}datum' % \
                                        ns.PSSERVICE, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}datum' % ns.PSSERVICE)

        if self.datum_type is not None:
            tree.set('type', self.datum_type)

        if self.contents is None:
            pass
        elif isinstance(self.contents, PsObject):
            self.contents.to_xml(tree, False)
        elif isinstance(self.contents, list):
            for cont in self.contents:
                if isinstance(cont, PsObject):
                    cont.to_xml(tree, False)

        if tostring is True:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
