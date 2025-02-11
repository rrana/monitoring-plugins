#!/usr/bin/env python3

import argparse
import requests
import sys


def check_elasticsearch_health(endpoint, port):
    url = f"http://{endpoint}:{port}/_cluster/health"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        status = data.get("status", "unknown")

        if status == "green":
            print(f"OK - Elasticsearch cluster is GREEN")
            sys.exit(0)
        elif status == "yellow":
            print(f"WARNING - Elasticsearch cluster is YELLOW")
            sys.exit(1)
        elif status == "red":
            print(f"CRITICAL - Elasticsearch cluster is RED")
            sys.exit(2)
        else:
            print(f"UNKNOWN - Elasticsearch cluster returned an unknown status: {status}")
            sys.exit(3)
    except requests.exceptions.RequestException as e:
        print(f"CRITICAL - Failed to connect to Elasticsearch: {e}")
        sys.exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios plugin to check Elasticsearch cluster health")
    parser.add_argument("--endpoint", required=True, help="Elasticsearch cluster endpoint")
    parser.add_argument("--port", type=int, required=True, help="Elasticsearch cluster port")
    args = parser.parse_args()

    check_elasticsearch_health(args.endpoint, args.port)
