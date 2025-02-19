# EC2 Volume Free Space Monitor for Nagios

This script checks the available free space on a given mount point and generates an alert if it falls below warning or critical thresholds.

## Requirements
- Python 3.x
- Works on Linux-based EC2 instances

## Installation
1. Copy `check_disk_space.py` to `/usr/local/bin/` and make it executable:
   ```bash
   sudo cp check_disk_space.py /usr/local/bin/check_disk_space
   sudo chmod +x /usr/local/bin/check_disk_space
   ```

## Usage
```
./check_disk_space.py -p /logs -w 5 -c 1

-p /logs → Path of the mount point to check
-w 5 → Warning threshold (GB)
-c 1 → Critical threshold (GB)

```

Output example:
```
OK: Free space on /logs is 12.50 GB
WARNING: Free space on /logs is 4.75 GB (below 5 GB)
CRITICAL: Free space on /logs is 0.95 GB (below 1 GB)
```

## Nagios integration

`commands.cfg`

```
define command {
    command_name check_disk_space
    command_line /usr/local/bin/check_disk_space -p $ARG1$ -w $ARG2$ -c $ARG3$
}
```

`services.cfg`

```
define service {
    use generic-service
    host_name your-ec2-instance
    service_description Check /logs Free Space
    check_command check_disk_space!/logs!5!1
}
```

Restart nagios

```
sudo systemctl restart nagios
```
