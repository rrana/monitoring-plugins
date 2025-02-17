#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timedelta

import boto3


def check_rds_restart(cluster_identifier, region):
    try:
        # Initialize AWS clients
        client = boto3.client("rds", region_name=region)

        # Calculate time range (last 30 minutes)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=30)

        # Fetch recent events for the RDS cluster
        response = client.describe_events(
            SourceType="db-cluster",
            SourceIdentifier=cluster_identifier,
            StartTime=start_time,
            EndTime=end_time
        )

        # Check for restart events
        restart_keywords = ["DB instance restarted", "DB cluster restarted", "DB engine version upgraded"]
        for event in response.get("Events", []):
            if any(keyword in event["Message"] for keyword in restart_keywords):
                print(f"CRITICAL - DB Restart detected: {event['Message']}")
                sys.exit(2)  # Nagios CRITICAL

        print(f"OK - No DB Restart detected in the last 30 minutes.")
        sys.exit(0)  # Nagios OK

    except Exception as e:
        print(f"UNKNOWN - Error occurred: {e}")
        sys.exit(3)  # Nagios UNKNOWN


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios Plugin: Check AWS RDS Aurora PostgreSQL Restart Events")
    parser.add_argument("--cluster", required=True, help="RDS Aurora Cluster Identifier")
    parser.add_argument("--region", required=True, help="AWS Region")
    
    args = parser.parse_args()
    check_rds_restart(args.cluster, args.region)
