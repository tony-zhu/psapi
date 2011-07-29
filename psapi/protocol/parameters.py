#!/usr/bin/env python

"""
Represents Parameters object
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

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            try:
                return object.__getattribute__(self, 'parameters')[name]
            except KeyError:
                raise AttributeError(name)
            
            

    @staticmethod
    def _parse_parameters(xml, cls, namespace):
        """
        Parse parameters with certin namespace and return an object of cls.
        """
        tree = PsObject.assert_xml(xml, '{%s}parameters' % namespace)
        object_id = tree.get('id')
        ref_id = None
        parameters = {}

        for param in tree.iterchildren():
            if param.tag == '{%s}parameter' % ns.NMWG:
                if len(param.getchildren()) > 0:
                    val = []
                    for param_child in param.getchildren():
                        parsed_param = PsObject.from_xml(param_child)
                        if parsed_param:
                            val.append(parsed_param)
                        else:
                            val.append('')
                    
                    if len(val) == 0:
                        val = ''
                    elif len(val) == 1:
                        val = val[0]
                    
                elif param.text:
                    val = param.text
                elif param.get('value'):
                    val = param.get('value')
                
                if param.get('name') in parameters:
                    if isinstance(parameters[param.get('name')], list):
                        parameters[param.get('name')].append(val)
                    else:
                        parameters[param.get('name')] = \
                                [parameters[param.get('name')], val]
                else:
                    parameters[param.get('name')] = val
            else:
                pass  # TODO: raise error or warn

        return cls(parameters, object_id, ref_id)
    
    def _parameters_to_xml(self, namespace, parent, tostring):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}parameters' % namespace, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}parameters' % namespace)

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
                if isinstance(self.parameters[itr], list):
                    for itr2 in self.parameters[itr]:
                        param = etree.SubElement(tree,
                                        '{%s}parameter' % ns.NMWG)
                        param.set('name', itr)
                        param.text = str(itr2)
                else:
                    param = etree.SubElement(tree, '{%s}parameter' % ns.NMWG)
                    param.set('name', itr)
                    param.text = str(self.parameters[itr])
        else:
            pass  # TODO: raise err or warn

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
        
    @staticmethod
    def from_xml(xml):
        return Parameters._parse_parameters(xml, Parameters, ns.NMWG)

    def to_xml(self, parent=None, tostring=True):
        return self._parameters_to_xml(ns.NMWG, parent, tostring)
