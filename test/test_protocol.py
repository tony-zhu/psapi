#!/usr/bin/env python
"""Unit testing from perfSONAR protocol object representations."""

import unittest
from psapi.protocol import PsObject
from psapi.protocol import EndPointPair
from psapi.protocol import Subject
from psapi.protocol import IPerfSubject
from psapi.protocol import Metadata
from psapi.protocol import Data
from psapi.protocol import Message
from psapi.protocol import events
from psapi.protocol import Parameters

class TestPsObject(unittest.TestCase):
    """Unit Testing for PsObject."""
    
    def test_init(self):
        """Test creating an object."""
        oid = 'TestId'
        ref_id = 'refID'
        pso = PsObject(object_id=oid, ref_id=ref_id)
        self.assertEqual(pso.object_id, oid)
        self.assertEqual(pso.ref_id, ref_id)
    
    def test_init_no_id(self):
        pso = PsObject()
        self.assertFalse(pso.object_id is None)
        self.assertTrue(pso.ref_id is None)
        self.assertTrue(isinstance(PsObject.generate_id(), str))
        
        self.assertTrue(pso.to_xml() is None)
        self.assertTrue(PsObject.from_xml('') is None)

class TestEndPointPair(unittest.TestCase):
    """Unit Testing for EndPointPair."""
    
    def setUp(self):
        self.oid = 'TestId'
        self.ref_id = 'refID'
        self.src = '128.128.128.128'
        self.src_type = 'ipv4'
        self.dst = 'dst.dst.com'
        self.dst_type = 'hostname'
        self.src2 = '129.129.129.129'
        self.dst2 = 'dst2.dst2.com'
        
    def test_init(self):
        ends = EndPointPair(src=self.src, dst=self.dst, \
                            object_id=self.oid, ref_id=self.ref_id)
        self.assertEqual(ends.src, self.src)
        self.assertEqual(ends.src_type, self.src_type)
        self.assertEqual(ends.dst, self.dst)
        self.assertEqual(ends.dst_type, self.dst_type)
        
    
    def test_eq(self):
        ends1 = EndPointPair(src=self.src, dst=self.dst, \
                            object_id=self.oid, ref_id=self.ref_id)
        ends2 = EndPointPair(src=self.src, dst=self.dst, \
                            object_id=self.oid, ref_id=self.ref_id)
        ends3 = EndPointPair(src=self.src2, dst=self.dst2, \
                            object_id=self.oid, ref_id=self.ref_id)
        
        self.assertEqual(ends1, ends2)
        self.assertNotEqual(ends1, ends3)
    
    def test_serialize(self):
        ends = EndPointPair(src=self.src, dst=self.dst, \
                            object_id=self.oid, ref_id=self.ref_id)
        # Read from string
        ends1 = EndPointPair.from_xml(ends.to_xml(tostring=True))
        self.assertEqual(ends1.src, self.src)
        self.assertEqual(ends1.src_type, self.src_type)
        self.assertEqual(ends1.dst, self.dst)
        self.assertEqual(ends1.dst_type, self.dst_type)
        
        #Read from etree Element
        ends2 = EndPointPair.from_xml(ends.to_xml(tostring=False))
        self.assertEqual(ends1, ends2)

class TestParameters(unittest.TestCase):
    """Unit Testing for Parameters."""
    
    def setUp(self):
        self.params = {'param1':'param1 val', 'param2':'param2 val'}
    
    def test_init(self):
        oid = 'ParamID'
        params1 = Parameters(self.params, 'ParamID')
        self.assertEqual(params1.parameters, self.params)
    
    def test_serialize(self):
        oid = 'ParamID'
        params1 = Parameters(self.params, 'ParamID')
        params2 = Parameters.from_xml(params1.to_xml(tostring=True))
        params3 = Parameters.from_xml(params1.to_xml(tostring=False))
        self.assertEqual(params1, params2)
        self.assertEqual(params1, params3)
        
        
                
class TestSubject(unittest.TestCase):
    """Unit Testing for Subject."""
    
    def setUp(self):
        src = '128.128.128.128'
        dst = 'dst.dst.com'
        src2 = '129.129.129.129'
        dst2 = 'dst2.dst2.com'
        self.ends1 = EndPointPair(src=src, dst=dst)
        self.ends2 = EndPointPair(src=src2, dst=dst2)
    
    def test_init(self):
        oid = 'TestId'
        ref_id = 'refID'
        
        subject1 = Subject(self.ends1, oid, ref_id)
        self.assertEqual(subject1.contents, self.ends1)
        self.assertEqual(subject1.object_id, oid)
        self.assertEqual(subject1.ref_id, ref_id)
        
        ends = [self.ends1, self.ends2]
        subject2 = Subject(ends, oid, ref_id)
        self.assertEqual(subject2.contents, ends)
        self.assertEqual(subject2.object_id, oid)
        self.assertEqual(subject2.ref_id, ref_id)
    
    def test_eq(self):
        oid = 'TestId'
        ref_id = 'refID'
        ends = [self.ends1, self.ends2]
        
        subject1 = Subject(self.ends1, oid, ref_id)
        subject2 = Subject(self.ends1, oid, ref_id)
        subject3 = Subject(ends, oid, ref_id)
        subject4 = Subject(ends, oid, ref_id)
        self.assertEqual(subject1, subject2)
        self.assertNotEqual(subject1, subject3)
        self.assertEqual(subject3, subject4)
        
    def test_serialize(self):
        oid = 'TestId'
        ref_id = 'refID'
        
        subject1 = Subject(self.ends1, oid, ref_id)
        subject2 = Subject.from_xml(subject1.to_xml(tostring=True))
        subject3 = Subject.from_xml(subject1.to_xml(tostring=False))
        self.assertEqual(subject1, subject2)
        self.assertEqual(subject1, subject3)

class TestIPerfSubject(unittest.TestCase):
    """Unit Testing for IPerfSubject."""
    
    def setUp(self):
        src = '128.128.128.128'
        dst = 'dst.dst.com'
        src2 = '129.129.129.129'
        dst2 = 'dst2.dst2.com'
        self.ends1 = EndPointPair(src=src, dst=dst)
        self.ends2 = EndPointPair(src=src2, dst=dst2)
    
    def test_init(self):
        oid = 'TestId'
        ref_id = 'refID'
        
        subject1 = IPerfSubject(self.ends1, oid, ref_id)
        self.assertEqual(subject1.contents, self.ends1)
        self.assertEqual(subject1.object_id, oid)
        self.assertEqual(subject1.ref_id, ref_id)
        
        ends = [self.ends1, self.ends2]
        subject2 = IPerfSubject(ends, oid, ref_id)
        self.assertEqual(subject2.contents, ends)
        self.assertEqual(subject2.object_id, oid)
        self.assertEqual(subject2.ref_id, ref_id)
    
    def test_eq(self):
        oid = 'TestId'
        ref_id = 'refID'
        ends = [self.ends1, self.ends2]
        
        subject1 = IPerfSubject(self.ends1, oid, ref_id)
        subject2 = IPerfSubject(self.ends1, oid, ref_id)
        subject3 = IPerfSubject(ends, oid, ref_id)
        subject4 = IPerfSubject(ends, oid, ref_id)
        self.assertEqual(subject1, subject2)
        self.assertNotEqual(subject1, subject3)
        self.assertEqual(subject3, subject4)
        
    def test_serialize(self):
        oid = 'TestId'
        ref_id = 'refID'
        
        subject1 = IPerfSubject(self.ends1, oid, ref_id)
        subject2 = IPerfSubject.from_xml(subject1.to_xml(tostring=True))
        subject3 = IPerfSubject.from_xml(subject1.to_xml(tostring=False))
        self.assertEqual(subject1, subject2)
        self.assertEqual(subject1, subject3)

class TestMetadata(unittest.TestCase):
    """Unit Testing for Subject."""
    
    def setUp(self):
        src = '128.128.128.128'
        dst = 'dst.dst.com'
        src2 = '129.129.129.129'
        dst2 = 'dst2.dst2.com'
        self.ends1 = EndPointPair(src=src, dst=dst)
        self.ends2 = EndPointPair(src=src2, dst=dst2)
        self.subject1 = Subject(self.ends1, 'sub1')
        self.subject2 = IPerfSubject([self.ends1, self.ends2], 'sub1')
        self.params = Parameters({'param1':'param1 val', \
                                    'param2':'param2 val'}, 'ParamID')
    
    def test_serialize(self):
        oid = 'TestId'
        ref_id = 'refID'
        meta1 = Metadata(self.subject1, event_types=events.IPERF2, \
                        parameters=self.params, \
                        object_id=oid, ref_id=ref_id)
        meta2 = Metadata(self.subject2, event_types=events.IPERF2, \
                        parameters=self.params, \
                        object_id=oid, ref_id=ref_id)
        
        meta3 = Metadata.from_xml(meta1.to_xml(tostring=True))
        meta4 = Metadata.from_xml(meta1.to_xml(tostring=False))
        
        meta5 = Metadata.from_xml(meta2.to_xml(tostring=True))
        meta6 = Metadata.from_xml(meta2.to_xml(tostring=False))
        
        self.assertEqual(meta1, meta3)
        self.assertEqual(meta1, meta4)
        
        self.assertNotEqual(meta1, meta2)
        
        self.assertEqual(meta2, meta5)
        self.assertEqual(meta2, meta6)
        
    
    def test_init(self):
        oid = 'TestId'
        ref_id = 'refID'
        meta = Metadata(self.subject1, event_types=events.IPERF2, \
                        parameters=self.params, \
                        object_id=oid, ref_id=ref_id)

class TestData(unittest.TestCase):
    """Unit Testing for Message."""
    
    def setUp(self):
        self.xml = open('test/xml/data.xml').read()
        
    def test_readxml(self):
        data = Data.from_xml(self.xml)
        self.assertTrue('http://ggf.org/ns/nmwg/tools/iperf/2.0/' \
                        in data.data)
                        
        data2 = Data.from_xml(data.to_xml(tostring=False))
        

class TestMessage(unittest.TestCase):
    """Unit Testing for Message."""
    
    def setUp(self):
        pass
        
    def test_readxml(self):
        xml = open('test/xml/message.xml').read()
        message = Message.from_xml(xml)
        
        f = open('/tmp/out.xml', 'w')
        f.write(message.to_xml())
        f.close()
        f.close()

        
if __name__ == "__main__":
    unittest.main()

