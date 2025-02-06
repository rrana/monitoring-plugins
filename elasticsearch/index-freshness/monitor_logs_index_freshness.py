#!/usr/bin/env python3

import sys
import argparse
import datetime
from elasticsearch import Elasticsearch, exceptions


# Nagios return codes
STATUS_OK = 0
STATUS_WARNING = 1
STATUS_CRITICAL = 2
STATUS_UNKNOWN = 3


def get_index_name(pattern):
    """Generate today's index name using the given pattern."""
    today = datetime.datetime.utcnow().strftime("%Y.%m.%d")
    return pattern.replace("{date}", today)


def check_elasticsearch_logs(es_host, index_pattern, time_window=5):
    """Check if new logs have been ingested in the last 'time_window' minutes."""
    try:
        es = Elasticsearch([es_host])

        # Generate index name for today
        index_name = get_index_name(index_pattern)

        # Define the time range query (last `time_window` minutes)
        now = datetime.datetime.utcnow()
        time_from = now - datetime.timedelta(minutes=time_window)

        query = {
            "query": {
                "range": {
                    "@timestamp": {  # Adjust timestamp field if necessary
                        "gte": time_from.strftime("%Y-%m-%dT%H:%M:%S"),
                        "lt": now.strftime("%Y-%m-%dT%H:%M:%S"),
                        "format": "strict_date_optional_time"
                    }
                }
            }
        }

        # Search for logs in the last `time_window` minutes
        response = es.search(index=index_name, body=query, size=1)

        # Process results
        total_logs = response["hits"]["total"]["value"]
        if total_logs > 0:
            print(f"OK: {total_logs} new logs found in {index_name} in the last {time_window} minutes.")
            return STATUS_OK
        else:
            print(f"CRITICAL: No logs found in {index_name} in the last {time_window} minutes.")
            return STATUS_CRITICAL

    except exceptions.ConnectionError:
        print("CRITICAL: Could not connect to Elasticsearch.")
        return STATUS_CRITICAL
    except exceptions.NotFoundError:
        print(f"WARNING: Index {index_name} not found.")
        return STATUS_WARNING
    except Exception as e:
        print(f"UNKNOWN: An unexpected error occurred: {str(e)}")
        return STATUS_UNKNOWN


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios plugin to check Elasticsearch log ingestion.")
    parser.add_argument("--host", required=True, help="Elasticsearch host (e.g., http://localhost:9200)")
    parser.add_argument("--index-pattern", required=True, help="Index naming pattern (e.g., 'server-request-logs-{date}')")
    parser.add_argument("--time-window", type=int, default=5, help="Time window in minutes (default: 5)")

    args = parser.parse_args()
    sys.exit(check_elasticsearch_logs(args.host, args.index_pattern, args.time_window))
