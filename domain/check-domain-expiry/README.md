# Domain Expiry Monitoring for Nagios

## Overview
This script checks the expiry date of a given domain and returns Nagios-compatible status codes.


## To manually check a domain:
```
python3 check_domain_expiry.py --domain example.com
```
Returns:
```
OK: Domain is not expiring soon.
WARNING: Domain expires within a week.
CRITICAL: Domain has already expired.
UNKNOWN: Unable to fetch data.
```

## Nagios config

`commands.cfg`

```
define command {
    command_name    check_domain_expiry
    command_line    /usr/bin/python3 /usr/local/nagios/libexec/check_domain_expiry.py --domain $ARG1$
}
```

`services.cfg`

```
define service {
    use                 generic-service
    host_name           your-host
    service_description Domain Expiry Check
    check_command       check_domain_expiry!example.com
    check_interval      1440  ; Runs once daily
    retry_interval      60
}
```


## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Move the script to Nagios' plugin directory:
   ```
   cp check_domain_expiry.py /usr/local/nagios/libexec/
   chmod +x /usr/local/nagios/libexec/check_domain_expiry.py
   ```
3. Configure Nagios by adding the provided command and service configuration.

4. Restart nagios
   ```
   systemctl restart nagios
   ```
