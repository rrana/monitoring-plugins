#!/usr/bin/env python3

import argparse
import boto3
import sys


region_name = 'us-east-1'

# for local testing
# aws_profile = 'myprofile'
# boto3.setup_default_session(profile_name=aws_profile)


def get_runnable_jobs(queue_name):
    client = boto3.client("batch", region_name=region_name)
    paginator = client.get_paginator("list_jobs")
    try:
        runnable_jobs_count = 0
        for page in paginator.paginate(jobQueue=queue_name, jobStatus="RUNNABLE"):
            runnable_jobs_count += len(page.get("jobSummaryList", []))
        return runnable_jobs_count
    except Exception as e:
        print(f"CRITICAL - Error fetching job queue data: {e}")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Nagios plugin to monitor AWS Batch job queue")
    parser.add_argument("-q", "--queue", required=True, help="AWS Batch Job Queue name")
    parser.add_argument("-t", "--threshold", type=int, required=True, help="Threshold for RUNNABLE jobs")
    args = parser.parse_args()

    queue_name = args.queue
    threshold = args.threshold

    runnable_jobs = get_runnable_jobs(queue_name)

    if runnable_jobs > threshold:
        print(f"CRITICAL - {runnable_jobs} jobs in RUNNABLE state (Threshold: {threshold})")
        sys.exit(2)
    else:
        print(f"OK - {runnable_jobs} jobs in RUNNABLE state (Threshold: {threshold})")
        sys.exit(0)


if __name__ == "__main__":
    main()
