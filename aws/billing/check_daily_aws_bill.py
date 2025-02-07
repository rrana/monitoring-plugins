#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timedelta, timezone

import boto3


region_name = 'us-east-1'

# for local testing
# aws_profile = '<profile-name>'
# boto3.setup_default_session(profile_name=aws_profile)


def get_previous_day_billing(account_id):
    client = boto3.client("ce", region_name=region_name)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    start_date = yesterday.strftime("%Y-%m-%d")
    end_date = (yesterday + timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        response = client.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            Filter={"Dimensions": {"Key": "LINKED_ACCOUNT", "Values": [account_id]}}
        )
        
        cost = float(response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])
        return cost
    except Exception as e:
        print(f"CRITICAL - Error fetching billing data: {e}")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Nagios plugin to monitor AWS billing")
    parser.add_argument("-a", "--account", required=True, help="AWS Account ID")
    parser.add_argument("-t", "--threshold", type=float, required=True, help="Billing threshold for the previous day")
    args = parser.parse_args()
    
    account_id = args.account
    threshold = args.threshold
    
    bill_amount = get_previous_day_billing(account_id)
    
    if bill_amount > threshold:
        print(f"CRITICAL - Previous day's bill is ${bill_amount:.2f} (Threshold: ${threshold:.2f})")
        sys.exit(2)
    else:
        print(f"OK - Previous day's bill is ${bill_amount:.2f} (Threshold: ${threshold:.2f})")
        sys.exit(0)


if __name__ == "__main__":
    main()
