#!/usr/bin/env python3

import boto3
import argparse
import time


# Exclude these queues from monitoring
EXCLUDED_QUEUES = [
    "queue_to_exclude_1",
    "queue_to_exclude_2",
    # Add more queues to exclude as needed
]


def get_queue_metrics(sqs_client, queue_url, period):
    """Retrieves the ApproximateNumberOfMessagesVisible metric for a queue."""

    end_time = int(time.time())
    start_time = end_time - period  # Period in seconds

    try:
        response = sqs_client.get_metric_data(
            Namespace='AWS/SQS',
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/SQS',
                            'MetricName': 'ApproximateNumberOfMessagesVisible',
                            'Dimensions': [
                                {'Name': 'QueueName', 'Value': queue_url.split('/')[-1]}  # Extract queue name
                            ]
                        },
                        'Period': 60,  # Granularity in seconds (adjust as needed)
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                },
            ],
            StartTime=start_time,
            EndTime=end_time
        )

        #Extract the datapoints and get the latest value
        datapoints = response['MetricDataResults'][0]['Values']
        if datapoints:
            return datapoints[-1] # Return the most recent value
        else:
            return 0  # No data points available, return 0

    except Exception as e:
        print(f"Error getting metrics for {queue_url}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Monitor SQS queue message backlog.")
    parser.add_argument("-p", "--period", type=int, default=300, help="Monitoring period in seconds (default: 300 seconds/5 minutes)")
    args = parser.parse_args()

    sqs = boto3.client('sqs')
    try:
        response = sqs.list_queues()
        queue_urls = response.get('QueueUrls', [])

        for queue_url in queue_urls:
            queue_name = queue_url.split('/')[-1]
            if queue_name in EXCLUDED_QUEUES:
                continue

            message_count = get_queue_metrics(sqs, queue_url, args.period)

            if message_count is not None:
                if message_count > 0:
                  print(f"CRITICAL: Queue {queue_name} has {message_count} messages visible.")
                  exit(2)  # Nagios CRITICAL status
                else:
                  print(f"OK: Queue {queue_name} has {message_count} messages visible.")
                  exit(0)  # Nagios OK status
            else:
                print(f"UNKNOWN: Could not retrieve metrics for {queue_name}.")
                exit(3)  # Nagios UNKNOWN status


    except Exception as e:
        print(f"UNKNOWN: Error listing queues: {e}")
        exit(3)  # Nagios UNKNOWN status


if __name__ == "__main__":
    main()
