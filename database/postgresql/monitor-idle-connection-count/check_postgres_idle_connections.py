#!/usr/bin/env python3

import argparse
import psycopg2
import sys


# Nagios plugin exit codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def get_idle_connection_count(dbname, host, port, user, password):
    """
    Connects to the PostgreSQL database and returns the count of idle connections.
    """
    try:
        # Establish database connection
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        # Query to count idle connections from pg_stat_activity
        cur.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'idle';")
        result = cur.fetchone()
        idle_count = result[0] if result else 0
        cur.close()
        conn.close()
        return idle_count
    except Exception as e:
        print("UNKNOWN - Error connecting to database: {}".format(e))
        sys.exit(UNKNOWN)


def main():
    parser = argparse.ArgumentParser(
        description="Nagios Plugin to monitor idle connection count on an Aurora PostgreSQL database."
    )
    parser.add_argument("dbname", help="Database name")
    parser.add_argument("db_endpoint", help="Database endpoint/host")
    parser.add_argument("db_port", type=int, help="Database port")
    parser.add_argument("db_username", help="Database username")
    parser.add_argument("db_password", help="Database password")
    parser.add_argument("threshold", type=int, help="Threshold for idle connection count (alert if exceeded)")

    args = parser.parse_args()

    # Get the current idle connection count from the database
    idle_count = get_idle_connection_count(
        dbname=args.dbname,
        host=args.db_endpoint,
        port=args.db_port,
        user=args.db_username,
        password=args.db_password
    )

    # Evaluate the count against the threshold and output the appropriate Nagios message and exit code
    if idle_count > args.threshold:
        print("CRITICAL - Idle connection count is {} (threshold: {})".format(idle_count, args.threshold))
        sys.exit(CRITICAL)
    else:
        print("OK - Idle connection count is {} (threshold: {})".format(idle_count, args.threshold))
        sys.exit(OK)


if __name__ == "__main__":
    main()
