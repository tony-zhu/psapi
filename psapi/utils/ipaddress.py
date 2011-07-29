"""
Helper methods for validating IP addresses,
Code borrowed from:
http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
"""

import re
hostname_re = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')

def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    return ipv4_re.match(ip) is not None


def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None


def is_valid_hostname(address):
    """
    Checks if the address is a valid hostname according to RFC1034#section-3.1
    """
    if len(address) > 255:
        return False
    if address[-1:] == ".":
        address = address[:-1]
    return all(hostname_re.match(x) for x in address.split("."))


def get_address_type(address):
    """Returns ipv4, ipv6, dns, url, or hostname"""
    if address is None:
        return None
    elif is_valid_ipv4(address):
        return 'ipv4'
    elif is_valid_ipv6(address):
        return 'ipv6'
    elif address.find("/") >= 0:
        return 'url'
    elif is_valid_hostname(address):
        # TODO Need better check for toplevel domain names
        address_len = len(address)
        if address[address_len-3] == '.' or address[address_len-4] == '.': 
            return 'dns'
        else:
            return 'hostname'
    else:
        return None
