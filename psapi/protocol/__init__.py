"""
NM & PerfSONAR protocol object representation  
"""

from psapi.protocol.psobject import PsObject
from psapi.protocol.endpointpair import EndPointPair
from psapi.protocol.interface import Interface
from psapi.protocol.parameters import Parameters
from psapi.protocol.selectparameters import SelectParameters
from psapi.protocol.summaryparameters import SummaryParameters
from psapi.protocol.subject import Subject
from psapi.protocol.iperfsubject import IPerfSubject
from psapi.protocol.owampsubject import OWAMPSubject
from psapi.protocol.traceroutesubject import TracerouteSubject
from psapi.protocol.selectsubject import SelectSubject
from psapi.protocol.snmpsubject import SNMPSubject
from psapi.protocol.netdiscardsubject import NetDiscardSubject
from psapi.protocol.neterrorsubject import NetErrorSubject
from psapi.protocol.netutilsubject import NetUtilSubject
from psapi.protocol.key import Key
from psapi.protocol.metadata import Metadata
from psapi.protocol.psdatum import PsDatum
from psapi.protocol.data import Data
from psapi.protocol.message import Message
from psapi.protocol.pssubject import PsSubject
from psapi.protocol.summarysubject import SummarySubject
from psapi.protocol.address import Address
from psapi.protocol.psservice import PsService
from psapi.protocol.nmbservice import NMBService
from psapi.protocol.xquerysubject import XQuerySubject
from psapi.protocol.xqueryparameters import XQueryParameters
from psapi.protocol.pingersubject import PingerSubject
from psapi.protocol.pingerparameters import PingerParameters


# Runtime objects registerations for each namespace

__namespace_mapper__ = {}

def register_namespace(namespace, class_def):
    """
    Register a class to represent a certain namespace object.
    
    for example:
        register_namespace('http://example.com/ns/service', ExampleService)
    then for all http://example.com/ns/service elements, ExampleService will
    be used to parse the element
    """
    __namespace_mapper__[namespace] = class_def


def get_namespace_class(namespace):
    """ Returns a class pointer to the class that represents the namespace."""
    return __namespace_mapper__.get(namespace, None)


## Register current defined objects
from psapi.protocol import namespaces as ns

register_namespace('{%s}parameters' % ns.NMWG, Parameters)
register_namespace('{%s}subject' % ns.NMWG, Subject)
register_namespace('{%s}metadata' % ns.NMWG, Metadata)
register_namespace('{%s}data' % ns.NMWG, Data)
register_namespace('{%s}message' % ns.NMWG, Message)
register_namespace('{%s}key' % ns.NMWG, Key)
register_namespace('{%s}endPointPair' % ns.NMWGT, EndPointPair)
register_namespace('{%s}interface' % ns.NMWGT, Interface)
register_namespace('{%s}parameters' % ns.XQUERY, XQueryParameters)
register_namespace('{%s}subject' % ns.XQUERY, XQuerySubject)
register_namespace('{%s}parameters' % ns.SELECT, SelectParameters)
register_namespace('{%s}subject' % ns.SELECT, SelectSubject)
register_namespace('{%s}parameters' % ns.PINGER, PingerParameters)
register_namespace('{%s}subject' % ns.PINGER, PingerSubject)
register_namespace('{%s}subject' % ns.IPERF2, IPerfSubject)
register_namespace('{%s}subject' % ns.OWAMP, OWAMPSubject)
register_namespace('{%s}subject' % ns.TRACEROUTE, TracerouteSubject)
register_namespace('{%s}subject' % ns.SNMP, SNMPSubject)
register_namespace('{%s}subject' % ns.NETDISC, NetDiscardSubject)
register_namespace('{%s}subject' % ns.NETERR, NetErrorSubject)
register_namespace('{%s}subject' % ns.NETUTIL, NetUtilSubject)
register_namespace('{%s}subject' % ns.SUMMARY, SummarySubject)
register_namespace('{%s}parameters' % ns.SUMMARY, SummaryParameters)
register_namespace('{%s}subject' % ns.PERFSONAR, PsSubject)
register_namespace('{%s}address' % ns.NMTB, Address)
register_namespace('{%s}service' % ns.PSSERVICE, PsService)
register_namespace('{%s}datum' % ns.PSSERVICE, PsDatum)
register_namespace('{%s}service' % ns.NMB, NMBService)
