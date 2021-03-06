#!/usr/bin/env python

"""
Define name spaces constants
"""

__authors__ = [
    '"Ahmed El-Hassany" <<ahassany@udel.edu>',
  ]

SOAP_ENCODE = "http://schemas.xmlsoap.org/soap/encoding/"
SOAP_ENVELOPE = "http://schemas.xmlsoap.org/soap/envelope/"
NMB = "http://ogf.org/schema/network/base/20070828/"
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
NETUTIL = 'http://ggf.org/ns/nmwg/characteristic/utilization/2.0/'
OWAMP = "http://ggf.org/ns/nmwg/tools/owamp/2.0/"
TRACEROUTE = 'http://ggf.org/ns/nmwg/tools/traceroute/2.0/'
XQUERY = 'http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/xquery/1.0/'
PINGER = 'http://ggf.org/ns/nmwg/tools/pinger/2.0/'
NMWGTOPO3 = 'http://ggf.org/ns/nmwg/topology/base/3.0/'
SNMP = "http://ggf.org/ns/nmwg/tools/snmp/2.0/" 
NETERR = "http://ggf.org/ns/nmwg/characteristic/errors/2.0/"
NETDISC = "http://ggf.org/ns/nmwg/characteristic/discards/2.0/"
GANGLIA = "http://ggf.org/ns/nmwg/tools/ganglia/2.0/"
 
# namespaces map to make the generated XML prettier!
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
nsmap['netutil'] = NETUTIL
nsmap['owamp'] = OWAMP
nsmap['traceroute'] = TRACEROUTE
nsmap['xquery'] = XQUERY 
nsmap['pinger'] = PINGER
nsmap['nmwgt3'] = NMWGTOPO3
nsmap['snmp'] = SNMP
nsmap['neterr'] = NETERR
nsmap['netdisc'] = NETDISC
nsmap['ganglia'] = GANGLIA

