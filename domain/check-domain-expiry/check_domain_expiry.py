#!/usr/bin/env python3

import whois
import argparse
import datetime
import sys


def check_domain_expiry(domain):
    try:
        domain_info = whois.whois(domain)
        expiry_date = domain_info.expiration_date
        
        if isinstance(expiry_date, list):  # Some WHOIS servers return a list
            expiry_date = expiry_date[0]

        if not expiry_date:
            print(f"UNKNOWN - Could not retrieve expiry date for {domain}")
            sys.exit(3)
        
        days_remaining = (expiry_date - datetime.datetime.utcnow()).days
        
        if days_remaining < 0:
            print(f"CRITICAL - Domain {domain} has already expired!")
            sys.exit(2)
        elif days_remaining <= 7:
            print(f"WARNING - Domain {domain} is expiring in {days_remaining} days!")
            sys.exit(1)
        else:
            print(f"OK - Domain {domain} expires in {days_remaining} days.")
            sys.exit(0)
    except Exception as e:
        print(f"UNKNOWN - Error checking domain {domain}: {str(e)}")
        sys.exit(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check domain expiry date")
    parser.add_argument("--domain", required=True, help="Domain to check")
    args = parser.parse_args()
    check_domain_expiry(args.domain)
