# Nagios Plugin: AWS ElastiCache Redis Monitoring

## Overview
This script checks if a Redis instance (hosted on AWS ElastiCache) is reachable by sending a `PING` command.

## Prerequisites
- Python 3.x
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

```
python3 check_redis.py --endpoint my-redis-cluster.abcdef.ng.0001.use1.cache.amazonaws.com
```

## Exit codes

```
0 (OK): Redis is reachable.
2 (CRITICAL): Redis is unreachable.
3 (UNKNOWN): Unexpected error.
```

## Nagios integration

1. Move the scrit to Nagios plugins directory
```
cp check_redis.py /usr/local/nagios/libexec/
chmod +x /usr/local/nagios/libexec/check_redis.py
```

2. Edit `commands.cfg`
```
define command {
    command_name    check_redis
    command_line    /usr/bin/python3 /usr/local/nagios/libexec/check_redis.py --endpoint $ARG1$
}
```

3. Edit `services.cfg`
```
define service {
    use                 generic-service
    host_name           your-host
    service_description Redis Health Check
    check_command       check_redis!my-redis-cluster.abcdef.ng.0001.use1.cache.amazonaws.com
    check_interval      5
    retry_interval      1
}
```

4. Restart Nagios
```
systemctl restart nagios
```
