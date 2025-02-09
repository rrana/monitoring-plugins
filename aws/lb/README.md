### Required IAM permissions
```
elasticloadbalancing:DescribeLoadBalancers
elasticloadbalancing:DescribeTargetGroups
elasticloadbalancing:DescribeTargetHealth
cloudwatch:GetMetricStatistics
```

### Usage
```
 python3 monitor_alb.py <load-balancer-name> <regions>

 ```

 Example outputs:
 ```
 $ python3 monitor_alb.py my-alb us-east-1
OK - ALB my-alb is healthy. 3/3 targets healthy. 5XX Errors: 0

$ python3 monitor_alb.py my-alb us-east-1
WARNING - 1/3 instances are unhealthy.

$ python3 monitor_alb.py my-alb us-east-1
CRITICAL - High HTTP 5XX errors detected: 12 in the last 5 minutes.
```

### Nagios customizations:
* Set up this script in Nagios by defining a Nagios command and service check.
* Adjust the error thresholds based on your environment.
* Schedule it to run every 5 minutes to detect issues quickly.

### How it works

* Retrieves ALB and associated Target Group:
    * Queries ALB details using `describe_load_balancers`.
    *  Finds its associated Target Group using `describe_target_groups`.

* Checks the Health of Target Group Instances:
    * Uses `describe_target_health` to count unhealthy instances.

* Monitors HTTP 5XX Errors (CloudWatch Metrics):
    * Fetches the count of `HTTPCode_ELB_5XX_Count` over the last 5 minutes.

* Nagios Integration:
    * `CRITICAL`: If all instances are unhealthy or 5XX errors exceed 10.
    * `WARNING`: If some instances are unhealthy or 5XX errors are detected (but not critical).
    * `OK`: If everything is running normally.
