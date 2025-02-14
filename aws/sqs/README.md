# SQS Queue Monitor

This script monitors AWS SQS queues for message backlog and is designed for use with Nagios.

## Requirements

- Python 3
- boto3 library (install with `pip install -r requirements.txt`)
- AWS credentials configured (e.g., via IAM role, environment variables, or shared credentials file).

## Installation

1.  Save the Python script as `check_sqs.py`.
2.  Install the required Python library: `pip install -r requirements.txt`.
3.  Ensure the script is executable: `chmod +x check_sqs.py`.
4.  Configure your Nagios server (see Nagios Configuration section).

## Usage

```bash
./check_sqs.py -p <period>
