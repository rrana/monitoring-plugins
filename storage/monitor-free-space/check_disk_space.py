#!/usr/bin/env python3

import os
import sys
import argparse


def get_free_space(mount_point):
    """Get free space in GB for the given mount point."""
    try:
        statvfs = os.statvfs(mount_point)
        free_space_gb = (statvfs.f_bavail * statvfs.f_frsize) / (1024 ** 3)  # Convert bytes to GB
        return free_space_gb
    except Exception as e:
        print(f"UNKNOWN: Unable to check disk space on {mount_point} - {e}")
        sys.exit(3)


def main():
    parser = argparse.ArgumentParser(description="Check disk space usage for Nagios")
    parser.add_argument("-p", "--path", required=True, help="Mount point to check (e.g., /logs)")
    parser.add_argument("-w", "--warning", type=float, required=True, help="Warning threshold (in GB)")
    parser.add_argument("-c", "--critical", type=float, required=True, help="Critical threshold (in GB)")
    
    args = parser.parse_args()

    free_space_gb = get_free_space(args.path)

    if free_space_gb < args.critical:
        print(f"CRITICAL: Free space on {args.path} is {free_space_gb:.2f} GB (below {args.critical} GB)")
        sys.exit(2)
    elif free_space_gb < args.warning:
        print(f"WARNING: Free space on {args.path} is {free_space_gb:.2f} GB (below {args.warning} GB)")
        sys.exit(1)
    else:
        print(f"OK: Free space on {args.path} is {free_space_gb:.2f} GB")
        sys.exit(0)


if __name__ == "__main__":
    main()
