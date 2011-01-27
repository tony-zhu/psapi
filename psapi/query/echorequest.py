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
    def __init__(self):
        self.default_message_type = Message.ECHO_REQUEST

    def get_psobjects(self):
        meta = Metadata(event_types=events.ECHO)
        data = Data(ref_id=meta.object_id)
        return {'meta':meta, 'data':data}