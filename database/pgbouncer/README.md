
# Example usage:

```
python3 check_pgbouncer.py -H 192.168.1.100 -p 6432 -d pgbouncer -U postgres -P mypassword
```

Nagios config:
```
Nagios command definition example:
define command{
    command_name    check_pgbouncer
    command_line    /usr/lib/nagios/plugins/pgbouncer_check.py -H $HOSTADDRESS$ -p 6432 -d pgbouncer -U postgres -P mypassword
}
```
