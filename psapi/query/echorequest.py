#!/usr/bin/env python

"""
Query Echo Request
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Data
from psapi.protocol import Message
from psapi.protocol import Metadata
from psapi.protocol import events
from psapi.query import Query


class EchoRequest(Query):
    """To check the liveness of perfSONAR service"""
    
    def __init__(self):
        Query.__init__(self, events.ECHO)
        self.default_message_type = Message.ECHO_REQUEST

    def get_psobjects(self):
        meta = Metadata(object_id=self._meta_object_id, event_types=events.ECHO)
        data = Data(object_id=self._data_object_id, ref_id=meta.object_id)
        return {'meta':meta, 'data':data}