#!/usr/bin/env python3

import sys
from pysnmp.hlapi import *


# Nagios plugin exit codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Define SNMP OIDs for common router metrics
OIDS = {
    "uptime": "1.3.6.1.2.1.1.3.0",
    "cpu_load": "1.3.6.1.4.1.2021.10.1.3.1",
    "mem_usage": "1.3.6.1.4.1.2021.4.6.0",  # Memory usage in KB
    "wan_in": "1.3.6.1.2.1.2.2.1.10.2",
    "wan_out": "1.3.6.1.2.1.2.2.1.16.2"


def snmp_get(target, community, oid):
    """Perform an SNMP GET request to retrieve a value."""
    try:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),  # SNMP v1/v2c
            UdpTransportTarget((target, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        
        if errorIndication:
            print("UNKNOWN - SNMP Error:", errorIndication)
            sys.exit(UNKNOWN)
        elif errorStatus:
            print(f"UNKNOWN - SNMP Error: {errorStatus.prettyPrint()}")
            sys.exit(UNKNOWN)
        else:
            return int(varBinds[0][1])
    except Exception as e:
        print(f"UNKNOWN - Failed to retrieve SNMP data: {e}")
        sys.exit(UNKNOWN)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 check_snmp.py <router_ip> <community_string>")
        sys.exit(UNKNOWN)

    router_ip = sys.argv[1]
    community_string = sys.argv[2]

    uptime = snmp_get(router_ip, community_string, OIDS["uptime"])
    cpu_load = snmp_get(router_ip, community_string, OIDS["cpu_load"])
    mem_usage = snmp_get(router_ip, community_string, OIDS["mem_usage"])
    wan_in = snmp_get(router_ip, community_string, OIDS["wan_in"])
    wan_out = snmp_get(router_ip, community_string, OIDS["wan_out"])

    # Print results
    print(f"OK - Uptime: {uptime} sec, CPU: {cpu_load}%, Mem: {mem_usage} KB, WAN In: {wan_in} bytes, WAN Out: {wan_out} bytes")
    sys.exit(OK)


if __name__ == "__main__":
    main()
