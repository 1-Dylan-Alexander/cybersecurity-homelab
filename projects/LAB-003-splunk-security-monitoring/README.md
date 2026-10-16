# LAB-003 — Splunk Security Monitoring

## Objective
Detect repeated Linux sudo authentication failures
using Splunk Enterprise and automated alerting.

## Environment
- Linux Mint 22.3
- Splunk Enterprise 10.6
- Linux PAM and sudo
- Authentication logs: /var/log/auth.log

## Lab Results
- Ingested Linux authentication logs.
- Extracted failed authentication counts with SPL.
- Detected 3 failed password attempts.
- Triggered a scheduled Medium-severity alert.

## Procedure
1. Configured continuous Linux authentication log monitoring.
2. Developed and tested an SPL detection rule.
3. Simulated repeated sudo authentication failures.
4. Verified the scheduled security alert triggered.

## Evidence
- [SPL Detection Rule](detections/repeated-sudo-failures.spl)
- [Investigation Report](evidence/investigation-report.md)

## Conclusion
Successfully validated automated sudo authentication
failure detection using Splunk Enterprise.
