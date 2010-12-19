#!/usr/bin/env python

"""
Define name spaces constants
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

SOAP_ENCODE = "http://schemas.xmlsoap.org/soap/encoding/"
SOAP_ENVELOPE = "http://schemas.xmlsoap.org/soap/envelope/"
NMTB = "http://ogf.org/schema/network/topology/base/20070828/"
NMTL3 = "http://ogf.org/schema/network/topology/l3/20070828/"
NMWG = "http://ggf.org/ns/nmwg/base/2.0/"
NMWGR = "http://ggf.org/ns/nmwg/result/2.0/"
NMWGT = "http://ggf.org/ns/nmwg/topology/2.0/"
OWAMP = "http://ggf.org/ns/nmwg/tools/owamp/2.0/"
PERFSONAR = "http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/"
PSSERVICE = "http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/"
SUMMARY = "http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/"
IPERF2 = "http://ggf.org/ns/nmwg/tools/iperf/2.0/"
SELECT = 'http://ggf.org/ns/nmwg/ops/select/2.0/'

# namspaces map to make the generated XML prettier!
nsmap = {}
nsmap['SOAP_ENCODE'] = SOAP_ENCODE
nsmap['SOAP_ENVELOPE'] = SOAP_ENVELOPE
nsmap['nmtb'] = NMTB
nsmap['nmtl3'] = NMTL3
nsmap['nmwg'] = NMWG
nsmap['nmwgr'] = NMWGR
nsmap['nmwgt'] = NMWGT
nsmap['owamp'] = OWAMP
nsmap['perfsonar'] = PERFSONAR
nsmap['psservice'] = PSSERVICE
nsmap['summary'] = SUMMARY
nsmap['iperf'] = IPERF2
nsmap['select'] = SELECT
