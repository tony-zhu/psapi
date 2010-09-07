"""Unit Tests for psapi.client.service.psprotocol.base.Metadata.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import unittest
from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Metadata

class MetadataTest(unittest.TestCase):
    
    def setUp(self):
        self.obj = PsObject()
        self.meta = Metadata(children=self.obj, id='meta.1', idref='message.1')
        pass
   
    def testCreateMessage(self):
        self.assertEqual(self.meta.id, 'meta.1')
        self.assertEqual(self.meta.idref, 'message.1')
        self.assertEqual(len(self.meta.children), 1)
        self.assertEqual(self.meta.children[0], self.obj)
        
    def testSerializeMessage(self):
        xml = self.meta.serialize()
        # Just to check it is a valid XML
        tree = etree.fromstring(xml)
        
        meta2 = Metadata.parse_xml(xml)
        self.assertEqual(self.meta, meta2)
        
