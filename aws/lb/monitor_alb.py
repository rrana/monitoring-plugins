#!/usr/bin/env python3

import sys
import boto3
import datetime


# Nagios plugin exit codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


# for local testing
# aws_profile = 'myprofile'
# boto3.setup_default_session(profile_name=aws_profile)


def get_alb_details(alb_name, region):
    """Fetches ALB ARN and Target Group ARN"""
    try:
        elb_client = boto3.client('elbv2', region_name=region)
        
        # Get ALB ARN
        alb_response = elb_client.describe_load_balancers()
        alb = next((lb for lb in alb_response['LoadBalancers'] if lb['LoadBalancerName'] == alb_name), None)
        if not alb:
            print(f"UNKNOWN - ALB {alb_name} not found.")
            sys.exit(UNKNOWN)
        
        alb_arn = alb['LoadBalancerArn']
        
        # Get Target Group associated with the ALB
        tg_response = elb_client.describe_target_groups(LoadBalancerArn=alb_arn)
        if not tg_response['TargetGroups']:
            print(f"UNKNOWN - No target groups associated with ALB {alb_name}.")
            sys.exit(UNKNOWN)

        return alb_arn, tg_response['TargetGroups'][0]['TargetGroupArn']
    except Exception as e:
        print(f"UNKNOWN - Failed to retrieve ALB details: {e}")
        sys.exit(UNKNOWN)


def check_target_health(target_group_arn, region):
    """Checks the health of instances in the target group"""
    try:
        elb_client = boto3.client('elbv2', region_name=region)
        response = elb_client.describe_target_health(TargetGroupArn=target_group_arn)
        
        unhealthy_count = 0
        for target in response['TargetHealthDescriptions']:
            if target['TargetHealth']['State'] != 'healthy':
                unhealthy_count += 1
        
        total_targets = len(response['TargetHealthDescriptions'])

        return unhealthy_count, total_targets
    except Exception as e:
        print(f"UNKNOWN - Failed to check target health: {e}")
        sys.exit(UNKNOWN)


def check_5xx_errors(alb_arn, region):
    """Fetches HTTP 5XX errors from AWS CloudWatch"""
    try:
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        
        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(minutes=5)  # Last 5 minutes

        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/ApplicationELB',
            MetricName='HTTPCode_ELB_5XX_Count',
            Dimensions=[{'Name': 'LoadBalancer', 'Value': alb_arn.split('/')[-1]}],
            StartTime=start_time,
            EndTime=now,
            Period=300,
            Statistics=['Sum']
        )

        data_points = response['Datapoints']
        error_count = sum(dp['Sum'] for dp in data_points) if data_points else 0

        return error_count
    except Exception as e:
        print(f"UNKNOWN - Failed to fetch 5XX error metrics: {e}")
        sys.exit(UNKNOWN)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 monitor_alb.py <ALB_NAME> <AWS_REGION>")
        sys.exit(UNKNOWN)

    alb_name = sys.argv[1]
    region = sys.argv[2]

    # Get ALB and Target Group details
    alb_arn, target_group_arn = get_alb_details(alb_name, region)

    # Check health of instances in the target group
    unhealthy_count, total_targets = check_target_health(target_group_arn, region)

    # Check ALB HTTP 5XX error count
    error_count = check_5xx_errors(alb_arn, region)

    # Determine Nagios status
    if unhealthy_count == total_targets:
        print(f"CRITICAL - All {total_targets} instances are unhealthy!")
        sys.exit(CRITICAL)
    elif unhealthy_count > 0:
        print(f"WARNING - {unhealthy_count}/{total_targets} instances are unhealthy.")
        sys.exit(WARNING)

    if error_count > 10:  # Adjust threshold based on environment
        print(f"CRITICAL - High HTTP 5XX errors detected: {error_count} in the last 5 minutes.")
        sys.exit(CRITICAL)
    elif error_count > 1:
        print(f"WARNING - Some HTTP 5XX errors detected: {error_count} in the last 5 minutes.")
        sys.exit(WARNING)

    print(f"OK - ALB {alb_name} is healthy. {total_targets - unhealthy_count}/{total_targets} targets healthy. 5XX Errors: {error_count}")
    sys.exit(OK)


if __name__ == "__main__":
    main()
