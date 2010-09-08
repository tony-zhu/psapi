"""Unit Tests for psapi.client.service.psprotocol.base.Metadata.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import unittest
from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Message
from psapi.client.service.psprotocol.base import Metadata

class MessageTest(unittest.TestCase):
    
    def setUp(self):
        self.obj = PsObject()
        self.meta = Metadata(children=self.obj, id='meta.1', idref='message.1')
        self.message = Message('request', self.meta, id='message.1')
        pass
   
    def testCreateMessage(self):
        self.assertEqual(self.message.id, 'message.1')
        self.assertEqual(self.message.idref, None)
        self.assertEqual(len(self.message.metadata), 1)
        self.assertTrue(isinstance(self.message.metadata[0], Metadata))
        
    def testSerializeMessage(self):
        xml = self.message.serialize()
        tree = etree.fromstring(xml)
        
        message2 = Message.parse_xml(xml)
        self.assertEqual(self.message, message2)
        
