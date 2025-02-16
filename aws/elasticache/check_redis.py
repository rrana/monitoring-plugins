#!/usr/bin/env python3

import argparse
import redis
import sys


def check_redis(endpoint):
    try:
        client = redis.Redis(host=endpoint, port=6379, socket_timeout=3)
        response = client.ping()
        if response:
            print(f"OK - Redis server at {endpoint} is reachable.")
            sys.exit(0)  # OK
        else:
            print(f"CRITICAL - Redis server at {endpoint} did not respond.")
            sys.exit(2)  # CRITICAL
    except redis.ConnectionError:
        print(f"CRITICAL - Unable to connect to Redis server at {endpoint}.")
        sys.exit(2)  # CRITICAL
    except Exception as e:
        print(f"UNKNOWN - Error occurred: {e}")
        sys.exit(3)  # UNKNOWN


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios Plugin: Check Redis Endpoint")
    parser.add_argument("--endpoint", required=True, help="Redis endpoint address (without port)")
    args = parser.parse_args()
    check_redis(args.endpoint)
