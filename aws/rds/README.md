# Nagios Plugin: AWS RDS Aurora PostgreSQL Restart Monitoring

## Overview
This script monitors AWS RDS Aurora PostgreSQL events for any **database restarts** within the last **30 minutes**.

## Prerequisites
- **Python 3.x**
- **AWS CLI configured** with permissions to `rds:DescribeEvents`
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage
```
python3 check_rds_restart.py --cluster my-aurora-cluster --region us-east-1
```

## Exit codes
```
0 (OK): No restart detected.
2 (CRITICAL): A restart event was detected.
3 (UNKNOWN): Error occurred.
```

## Nagios integration

`commands.cfg`
```
define command {
    command_name    check_rds_restart
    command_line    /usr/bin/python3 /usr/local/nagios/libexec/check_rds_restart.py --cluster $ARG1$ --region $ARG2$
}
```

`services.cfg`
```
define service {
    use                 generic-service
    host_name           your-host
    service_description AWS RDS Aurora PostgreSQL Restart Check
    check_command       check_rds_restart!my-aurora-cluster!us-east-1
    check_interval      10
    retry_interval      2
}
```

Restart nagios
```
systemctl restart nagios
```
