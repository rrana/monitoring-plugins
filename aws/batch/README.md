### How it works

```
chmod +x check_aws_batch.py
./check_aws_batch.py -q <batch-queue-name> -t 5
```

This checks if the given queue (-q <batch-queue-name>) has more than 5 RUNNABLE jobs.

Exit Codes:
0 (OK): Jobs count is below the threshold.
2 (CRITICAL): Jobs count exceeds the threshold.

This script is compatible with Nagios and can be used as a plugin for monitoring AWS Batch job queues. 
