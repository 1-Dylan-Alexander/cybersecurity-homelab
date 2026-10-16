# LAB-003 — Security Investigation Report

## Investigation Overview

- Date: October 16, 2026
- SIEM: Splunk Enterprise 10.6
- Operating System: Linux Mint 22.3
- Monitored Host: mint-t480-lab
- Log Source: /var/log/auth.log
- Sourcetype: linux_secure
- Alert Severity: Medium
- Classification: Authorized Security Simulation

## Objective

Detect repeated failed sudo authentication attempts
using Linux authentication logs and Splunk SPL.

## Tools and Technologies

- Splunk Enterprise 10.6
- Linux Mint 22.3
- Linux PAM
- sudo
- Splunk Processing Language (SPL)

## Event Timeline

| Time (PDT) | Event |
|---|---|
| 14:14:40 | PAM authentication failure recorded |
| 14:14:47 | Sudo reported 3 incorrect password attempts |
| 14:20:00 | Scheduled Splunk security alert triggered |

## Detection Methodology

Splunk monitored /var/log/auth.log continuously.

SPL extracted failed password counts from sudo logs.
Events were grouped by host, account, and
fixed five-minute intervals.

Detection threshold: 3 failed attempts.
Alert schedule: Every 5 minutes.
Search window: -10m@m to -5m@m.
Alert severity: Medium.

## Investigation Findings

1. Splunk successfully ingested Linux authentication logs.
2. PAM recorded a failed authentication.
3. Sudo reported three incorrect password attempts.
4. SPL extracted and aggregated the failure count.
5. The detection threshold was reached.
6. A Medium-severity alert triggered at 14:20 PDT.

## Security Assessment

The activity was an authorized simulation.
No unauthorized access was established.

## Detection Limitations

- Detects sudo summary messages only.
- Does not cover SSH authentication failures.
- Uses fixed five-minute intervals.
- Does not identify every failed password attempt.
- Log rotation requires further testing.

## Conclusion

LAB-003 demonstrated successful Linux log ingestion,
SPL analysis, and automated security alerting.

Splunk detected three simulated failed sudo password
attempts and triggered a Medium-severity alert.

The activity was authorized and controlled.
