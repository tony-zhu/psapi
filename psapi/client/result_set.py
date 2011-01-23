#!/usr/bin/env python
"""
perfSONAR Result set.
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

from psapi.protocol import Key
from psapi.protocol import PsSubject
from psapi.protocol import Metadata
from psapi.protocol import Message


class ResultSet(object):
    """perfSONAR queries returns Message Object. This object makes it
    eaiser to read the results."""
    def __init__(self, meta, data):
        self.meta = meta
        self.data = data

    @staticmethod
    def parse_result(result):
        if isinstance(result, Message):
            message = result
        else:
            message = Message.from_xml(result)

        meta = {}
        data = {}
        if not isinstance(message.meta, list):
            message.meta = [message.meta]

        if not isinstance(message.data, list):
            message.data = [message.data]

        for m in message.meta:
            meta[m.object_id] = m

        for d in message.data:
            tmp = d.data

            # Formatting for to make accessing the data easier
            if isinstance(tmp, dict):
                if len(tmp) == 1:
                    tmp = tmp.items()[0][1]

            # if the query is meta key request, just extract the key
            if isinstance(tmp, Key):
                if tmp.parameters.maKey is not None:
                    tmp = tmp.parameters.maKey

            # if the query is lookup request, just extract the service
            if isinstance(tmp, Metadata):
                if isinstance(tmp.subject, PsSubject):
                    tmp = tmp.subject.contents

            if d.ref_id in data:
                if isinstance(data[d.ref_id], list):
                    data[d.ref_id].append(tmp)
                else:
                    data[d.ref_id] = [data[d.ref_id], tmp]
            else:
                data[d.ref_id] = tmp

        if len(meta) == 1 and len(data) == 1:
            meta = meta.items()[0][1]
            data = data.items()[0][1]

        return ResultSet(meta, data)
