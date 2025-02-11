### How to use this script

```
python3 check_es_cluster_health.py --endpoint <elasticsearch_host> --port <elasticsearch_port>

```

## Nagios setup

command definition:
```
define command {
    command_name    check_es_cluster
    command_line    /usr/local/nagios/libexec/check_es_cluster_health.py --endpoint $ARG1$ --port $ARG2$
}
```

service check definition:
```
define service {
    use                 generic-service
    host_name           your-host
    service_description Elasticsearch Cluster Health
    check_command       check_es_cluster!localhost!9200
}
```
