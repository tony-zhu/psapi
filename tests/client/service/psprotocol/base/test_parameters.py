"""Unit Tests for psapi.client.service.psprotocol.base.Parameters.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import unittest
from lxml import etree

from psapi.client.service import namespaces as ns
from psapi.client.service.psprotocol import PsObject
from psapi.client.service.psprotocol.base import Parameter
from psapi.client.service.psprotocol.base import Parameters

class ParametersTest(unittest.TestCase):
    
    def setUp(self):
        self.obj = PsObject()
        self.param1 = Parameter(name='parameter1', value='value1',
                                nested='param1 nested value')
        self.param2 = Parameter(name='parameter2', value='value2',
                                nested='param2 nested value')
        self.params = Parameters([self.param1, self.param2], id='params.1')
   
    def testCreateMessage(self):
        self.assertEqual(self.params.id, 'params.1')
        self.assertEqual(len(self.params.parameters), 2)
        self.assertEqual(self.params.parameters[self.param1.name], self.param1)
        self.assertEqual(self.params.parameters[self.param2.name], self.param2)
        
    def testSerializeMessage(self):
        xml = self.params.serialize()
        # Just to check it is a valid XML
        tree = etree.fromstring(xml)
        
        params2 = Parameters.parse_xml(xml)
        self.assertEqual(self.params, params2)
        
