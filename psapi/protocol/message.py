#!/usr/bin/env python
"""
Represents Message object
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from lxml import etree

from psapi.protocol import PsObject
from psapi.protocol import Metadata
from psapi.protocol import Parameters
from psapi.protocol import namespaces as ns


class Message(PsObject):
    """nmwg:message object."""

    #Define perfSONAR message types
    DATA_INFO_REQUEST = 'DataInfoRequest'
    DATA_INFO_RESPONSE = 'DataInfoResponse'
    ECHO_RQUEST = 'EchoRequest'
    ECHO_RESPONSE = 'EchoResponse'
    METADATA_KEY_REQUEST = 'MetadataKeyRequest'
    METADATA_KEY_RESPONSE = 'MetadataKeyResponse'
    SETUP_DATA_REQUEST = 'SetupDataRequest'
    SETUP_DATE_RESPONSE = 'SetupDataResponse'

    def __init__(self, meta=None, data=None, message_type=None, \
                parameters=None, object_id=None, ref_id=None):
        """
        meta and data can be list of Metadata and Data objects but it
        has to be of the same length.
        """
        PsObject.__init__(self, object_id, ref_id)
        self.meta = meta
        self.data = data
        self.message_type = message_type
        self.parameters = parameters

    @staticmethod
    def from_xml(xml):
        tree = PsObject.assert_xml(xml, '{%s}message' % ns.NMWG)
        object_id = tree.get('id')
        ref_id = tree.get('messageIdRef')
        message_type = tree.get('type')
        meta = []
        data = []
        parameters = None

        for child in tree.iterchildren():
            obj = PsObject.from_xml(child)
            if isinstance(obj, Metadata):
                meta.append(obj)
            elif isinstance(obj, Parameters):
                parameters = obj
            else:
                data.append(obj)

        if len(meta) == 0:
            meta = None
        elif len(meta) == 1:
            meta = meta[0]

        if len(data) == 0:
            data = None
        elif len(data) == 1:
            data = data[0]

        return Message(meta, data, message_type, parameters, \
                       object_id, ref_id)

    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        if parent is None:
            tree = etree.Element('{%s}message' % ns.NMWG, nsmap=ns.nsmap)
        else:
            tree = etree.SubElement(parent, '{%s}message' % ns.NMWG)

        if self.object_id is None:
            self.object_id = PsObject.generate_id()

        tree.set('id', self.object_id)

        if self.ref_id is not None:
            tree.set('messageIdRef', self.ref_id)

        if self.message_type is not None:
            tree.set('type', self.message_type)

        if hasattr(self.meta, 'to_xml'):
            self.meta.to_xml(tree, False)
        elif isinstance(self.meta, list):
            for meta in self.meta:
                if hasattr(meta, 'to_xml'):
                    meta.to_xml(tree, False)

        if hasattr(self.data, 'to_xml'):
            self.data.to_xml(tree, False)
        elif isinstance(self.data, list):
            for data in self.data:
                if hasattr(data, 'to_xml'):
                    data.to_xml(tree, False)

        if hasattr(self.parameters, 'to_xml'):
            self.parameters.to_xml(tree, False)

        if tostring:
            return etree.tostring(tree, pretty_print=True)
        else:
            return tree
