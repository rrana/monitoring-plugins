#!/usr/bin/env python3
import argparse
import psycopg2
import sys


# Nagios plugin exit codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def get_connection_count(dbname, host, port, user, password):
    """Connects to the database and returns the number of connections."""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        # Query to count all connections from pg_stat_activity
        cur.execute("SELECT COUNT(*) FROM pg_stat_activity;")
        result = cur.fetchone()
        connection_count = result[0] if result else 0
        cur.close()
        conn.close()
        return connection_count
    except Exception as e:
        print("UNKNOWN - Error connecting to database: {}".format(e))
        sys.exit(UNKNOWN)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Aurora PostgreSQL connection count for Nagios."
    )
    parser.add_argument("dbname", help="Database name")
    parser.add_argument("db_endpoint", help="Database endpoint/host")
    parser.add_argument("db_port", type=int, help="Database port")
    parser.add_argument("db_username", help="Database username")
    parser.add_argument("db_password", help="Database password")
    parser.add_argument("threshold", type=int, help="Threshold for connection count (if exceeded, alert is raised)")

    args = parser.parse_args()

    # Get the current connection count
    connection_count = get_connection_count(
        dbname=args.dbname,
        host=args.db_endpoint,
        port=args.db_port,
        user=args.db_username,
        password=args.db_password
    )

    # Check against the threshold and output the appropriate Nagios message and exit code
    if connection_count > args.threshold:
        print("CRITICAL - Connection count is {} (threshold: {})".format(connection_count, args.threshold))
        sys.exit(CRITICAL)
    else:
        print("OK - Connection count is {} (threshold: {})".format(connection_count, args.threshold))
        sys.exit(OK)


if __name__ == "__main__":
    main()
