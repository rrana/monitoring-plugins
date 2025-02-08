### How it works

```
python3 check_postgres_idle_connections.py <db_name> <db_endpoint> <db_port> <db_username> <db_password> <threshold>
````

Command-Line Arguments:
The script accepts the following parameters:

dbname: Name of the database.
db_endpoint: Host or endpoint of the Aurora PostgreSQL instance.
db_port: Port number.
db_username: Username for the database.
db_password: Password for the database.
threshold: Maximum allowed idle connection count before raising an alert.


Database Query:
It connects to the database and runs:

```
SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'idle';
```
This returns the total number of idle connections.

Nagios Plugin Behavior:

If the idle connection count exceeds the provided threshold, the script prints a CRITICAL message and exits with code 2.
Otherwise, it prints an OK message and exits with code 0.
Any errors (like connection issues) result in an UNKNOWN state (exit code 3).

This script can be integrated into Nagios as a plugin to continuously monitor your Aurora PostgreSQL database for idle connections.
