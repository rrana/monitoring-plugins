#!/usr/bin/env python3

import argparse
import sys

import psycopg2


def check_pgbouncer_health(host, port, dbname, user, password):
    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()
        cur.execute("SHOW STATS")
        cur.fetchall()
        cur.close()
        conn.close()
        print("OK - PgBouncer is healthy")
        sys.exit(0)
    except Exception as e:
        print(f"CRITICAL - PgBouncer health check failed: {e}")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Nagios plugin to monitor PgBouncer health")
    parser.add_argument("-H", "--host", required=True, help="PgBouncer instance IP or hostname")
    parser.add_argument("-p", "--port", required=True, type=int, help="PgBouncer port")
    parser.add_argument("-d", "--dbname", required=True, help="Database name")
    parser.add_argument("-U", "--user", required=True, help="Database user")
    parser.add_argument("-P", "--password", required=True, help="Database password")
    args = parser.parse_args()
    
    check_pgbouncer_health(args.host, args.port, args.dbname, args.user, args.password)


if __name__ == "__main__":
    main()
