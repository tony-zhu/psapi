#!/usr/bin/env python

"""Represents Parameters object
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import namespaces as ns


class Parameters(PsObject):
    """nmwg:parameters object.
    paramters has to be a dict of key/value pairs.
    """
    def __init__(self, parameters=None, object_id=None, ref_id=None):
        PsObject.__init__(self, object_id, ref_id)
        self.parameters = parameters

    def __eq__(self, other):
        if not isinstance(other, Parameters):
            return False
        if self.object_id != other.object_id:
            return False
        if self.ref_id != other.ref_id:
            return False
        if self.parameters != other.parameters:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattribute__(self,name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            try:
                return object.__getattribute__(self, 'parameters')[name]
            except KeyError:
                raise AttributeError(name)
            
            

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}parameters' % ns.NMWG)
        object_id = tree.get('id')
        ref_id = None
        parameters = {}

        for param in tree.iterchildren():
            if param.tag == '{%s}parameter' % ns.NMWG:
                if param.text is None:
                    val = param.get('value')
                else:
                    val = param.text
                parameters[param.get('name')] = val
            else:
                pass  # TODO: raise error or warn

        return Parameters(parameters, object_id, ref_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}parameters' % ns.NMWG, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}parameters' % ns.NMWG)

        if self.object_id is None:
            self.object_id = PsObject.generate_id()

        tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('metadataIdRef', self.ref_id)

        # Parameters
        if self.parameters is None:
            pass
        elif isinstance(self.parameters, dict):
            for itr in self.parameters:
                param = etree.SubElement(tree, '{%s}parameter' % ns.NMWG)
                param.set('name', itr)
                param.text = str(self.parameters[itr])
        else:
            pass  # TODO: raise err or warn

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
