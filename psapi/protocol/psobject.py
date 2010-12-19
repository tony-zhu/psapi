#!/usr/bin/env python
"""
A generic parent object for perfSONAR objects.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

import random

class PsObject(object):
    """Any perfSONAR objects contains two basic fields(id, referenceId).
    """
    def __init__(self, object_id=None, ref_id=None):
        """Initialize new PsObject."""
        if object_id is None:
            self.object_id = PsObject.generate_id()
        else:
            self.object_id = object_id
        self.ref_id = ref_id
    
    def to_xml(self, parent=None, tostring=True):
        """Serialize to XML representation."""
        pass
    
    @staticmethod
    def from_xml(xml):
        """Creates PsObject from XML input."""
        pass
    
    @staticmethod
    def generate_id():
        """Generates new random ID."""
        return "GenID.%i" % random.randint(100, 100000000)
