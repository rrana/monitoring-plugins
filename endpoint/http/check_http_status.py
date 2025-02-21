#!/usr/bin/env python3

import argparse
import requests
import sys


def check_http_status(endpoint, expected_status):
    try:
        response = requests.get(endpoint, timeout=10)
        if response.status_code == expected_status:
            print(f"OK - {endpoint} is up and returned {response.status_code}")
            sys.exit(0)  # Nagios OK
        else:
            print(f"CRITICAL - {endpoint} returned {response.status_code}, expected {expected_status}")
            sys.exit(2)  # Nagios CRITICAL
    except requests.exceptions.RequestException as e:
        print(f"CRITICAL - Error reaching {endpoint}: {e}")
        sys.exit(2)  # Nagios CRITICAL


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios HTTP status monitor")
    parser.add_argument("endpoint", help="HTTP/HTTPS endpoint to check")
    parser.add_argument("expected_status", type=int, help="Expected HTTP status code")

    args = parser.parse_args()
    check_http_status(args.endpoint, args.expected_status)
