#!/usr/bin/env python3


import argparse
import sys

import boto3


def check_beanstalk_health(environment_name, region):
    try:
        # Initialize AWS Elastic Beanstalk client
        client = boto3.client("elasticbeanstalk", region_name=region)

        # Get environment health
        response = client.describe_environment_health(
            EnvironmentName=environment_name,
            AttributeNames=["HealthStatus"]
        )

        health_status = response.get("HealthStatus", "Unknown")

        if health_status == "Ok":
            print(f"OK - Beanstalk environment '{environment_name}' is healthy.")
            sys.exit(0)  # Nagios OK
        elif health_status == "Warning":
            print(f"WARNING - Beanstalk environment '{environment_name}' is in a warning state.")
            sys.exit(1)  # Nagios WARNING
        else:
            print(f"CRITICAL - Beanstalk environment '{environment_name}' is unhealthy ({health_status}).")
            sys.exit(2)  # Nagios CRITICAL

    except Exception as e:
        print(f"UNKNOWN - Error occurred: {e}")
        sys.exit(3)  # Nagios UNKNOWN


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nagios Plugin: Check AWS Elastic Beanstalk Environment Health")
    parser.add_argument("--environment", required=True, help="Elastic Beanstalk Environment Name")
    parser.add_argument("--region", required=True, help="AWS Region")

    args = parser.parse_args()
    check_beanstalk_health(args.environment, args.region)
