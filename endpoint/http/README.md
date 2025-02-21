## How it works

Install requirements.
```
pip install -r requirements.txt
pip install -r requirements.txt
```

## Usage
```
./check_http_status.py https://example.com 200
```

## Nagios Integration

Copy plugin:
```
cp check_http_status.py /usr/local/nagios/libexec/
chmod +x /usr/local/nagios/libexec/check_http_status.py
```

Update `services.cfg`

```
define service {
    use                 generic-service
    host_name           my-server
    service_description HTTP Endpoint Check
    check_command       check_http_status!https://example.com!200
}
```

Update `commands.cfg`
```
define command {
    command_name check_http_status
    command_line /usr/local/nagios/libexec/check_http_status.py $ARG1$ $ARG2$
}
```

Restart nagios:
```
systemctl restart nagios
```
