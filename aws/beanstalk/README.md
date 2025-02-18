# Nagios Plugin: AWS Elastic Beanstalk Health Monitoring

## Overview
This script monitors the health of an **AWS Elastic Beanstalk environment** and checks if it is in an **"Ok" (healthy) state**.

## Prerequisites
- **Python 3.x**
- **AWS CLI configured** with access to `elasticbeanstalk:DescribeEnvironmentHealth`
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

```
python3 check_beanstalk_health.py --environment my-environment --region us-east-1
```

## Exit codes

```
0 (OK): Beanstalk environment is healthy.
1 (WARNING): Environment is in a warning state.
2 (CRITICAL): Environment is unhealthy.
3 (UNKNOWN): Error occurred.
```

## Nagios Integration

```
cp check_beanstalk_health.py /usr/local/nagios/libexec/
chmod +x /usr/local/nagios/libexec/check_beanstalk_health.py
```

`commands.cfg`
```
define command {
    command_name    check_beanstalk_health
    command_line    /usr/bin/python3 /usr/local/nagios/libexec/check_beanstalk_health.py --environment $ARG1$ --region $ARG2$
}
```

`services.cfg`
```
define service {
    use                 generic-service
    host_name           your-host
    service_description AWS Beanstalk Environment Health
    check_command       check_beanstalk_health!my-environment!us-east-1
    check_interval      5
    retry_interval      2
}
```

Restart nagios
```
systemctl restart nagios
```