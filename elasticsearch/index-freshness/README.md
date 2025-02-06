### How to use this script

```

./monitor_logs_index_freshness.py --host http://<es-endpoint>:<port> --index-pattern "<index-name-{date}>"

Output pattern:
ok state:
OK: 25 new logs found in server-request-logs-2025.02.06 in the last 5 minutes.

critical state:
CRITICAL: No logs found in server-request-logs-2025.02.06 in the last 5 minutes.
```

### nagios config:

```
/etc/nagios/objects/commands.cfg

define command {
    command_name check_es_index_freshness
    command_line /usr/lib/nagios/plugins/monitor_logs_index_freshness.py --host $ARG1$ --index-pattern $ARG2$ --time-window $ARG3$
}


/etc/nagios/objects/services.cfg

define service {
    use                 generic-service
    host_name           my-elasticsearch-host
    service_description Elasticsearch Log Ingestion Check
    check_command       check_es_index_freshness!http://my-es-cluster:9200!server-request-logs-{date}!5
}

restart nagios:
systemctl restart nagios

```
