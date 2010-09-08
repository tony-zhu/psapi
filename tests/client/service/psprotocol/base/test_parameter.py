"""Unit Tests for psapi.client.service.psprotocol.base.Parameter.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import unittest
from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Parameter

class ParameterTest(unittest.TestCase):
    
    def setUp(self):
        self.obj = PsObject()
        self.param = Parameter(name='parameter1', value='value1',
                                nested='param nested value')
        pass
   
    def testCreateMessage(self):
        self.assertEqual(self.param.name, 'parameter1')
        self.assertEqual(self.param.value, 'value1')
        self.assertEqual(self.param.nested, 'param nested value')
        
    def testSerializeMessage(self):
        xml = self.param.serialize()
        # Just to check it is a valid XML
        tree = etree.fromstring(xml)
        
        param2 = Parameter.parse_xml(xml)
        self.assertEqual(self.param, param2)
        
