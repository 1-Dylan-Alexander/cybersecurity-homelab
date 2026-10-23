# LAB-004 — Incident Response and Digital Forensics: Windows RDP Intrusion Simulation

> **Environment:** Isolated, authorized cybersecurity homelab  
> **Assessment:** Completed simulation, SIEM investigation, native event-log acquisition, and SHA-256 integrity verification  
> **Case date:** 2026-10-19 (local times: Pacific Daylight Time)

## Executive investigation summary

An authorized Kali-to-Windows RDP exercise generated Windows Security logon events (4625/4624), PowerShell and scheduled-task activity, and Sysmon process/file telemetry (IDs 1/11). These records were correlated in Splunk to produce a timeline. Native `.evtx` exports were hashed before transfer and their USB copies verified with SHA-256. This exercise **did not involve an actual attacker, unauthorized compromise, or confirmed malicious persistence**.

**Reviewer links:** [← Portfolio home](../../README.md) · [Detailed investigation report](reports/investigation-report.md) · [Evidence publication boundaries](../../docs/evidence-handling.md)

## Objectives

- Generate and investigate a realistic sequence of Windows authentication and post-login activity in an isolated lab.
- Correlate Windows Security and Sysmon telemetry in Splunk Enterprise.
- Distinguish failed authentication, valid-credential RDP access, PowerShell execution, and scheduled-task behavior.
- Acquire original-format Windows event-log exports, verify copied evidence with SHA-256, and produce an incident timeline.
- Document what the telemetry supports **without representing authorized activity as an actual compromise**.

## Environment and tools

| Component | Role |
| --- | --- |
| Linux Mint 22.3 host | VirtualBox hypervisor, Splunk Enterprise 10.6.0.5, evidence-transfer host |
| Kali Linux VM — `192.168.56.102` | Authorized RDP client and simulated originating host |
| Windows 11 Enterprise Evaluation VM — `192.168.56.104` | Investigation endpoint / RDP server (`DESKTOP-TH2SL52`) |
| VirtualBox host-only network — `192.168.56.0/24` | Isolated lab communication |
| Sysmon | Process-creation (ID 1), file-creation (ID 11), and other endpoint telemetry |
| Splunk Universal Forwarder | Sends Windows Security and Sysmon logs to Splunk receiver at `192.168.56.1:9997` |
| Splunk Search & Reporting | Event correlation, filtering, and timeline construction |
| Windows `schtasks.exe` | Benign scheduled-task persistence emulation |
| Windows `wevtutil`, PowerShell `Get-FileHash`, Linux `sha256sum` | Evidence acquisition and integrity verification |
| 32 GB exFAT USB, label `DFIR-LAB004` | Offline removable-media evidence copies |

**Scope and safety:** All actions were carried out against the user's own isolated Windows VM with authorized credentials. Kali and Windows communicated over VirtualBox host-only networking; the scenario did not exploit a vulnerability or involve a real adversary. A pre-simulation snapshot (`LAB004-BASELINE-PRE-ATTACK`) was taken.

## Procedure

1. **Telemetry baseline:** Enabled Windows Security logon success/failure auditing and Sysmon. Confirmed Sysmon process creation and file creation events, forwarded via Splunk Universal Forwarder into Splunk Enterprise.
2. **Network setup:** Restricted RDP firewall access to Kali (`192.168.56.102`); confirmed the virtualized RDP target was reachable.
3. **Failed authentication:** An initial FreeRDP authentication request was automatically submitted without a manually entered wrong password. Windows recorded **Security 4625** for `dylan`, NTLM, Logon Type 3, substatus `0xC000006A`. Do not characterize this as a manually entered incorrect password or brute-force attempt.
4. **Authorized session:** Established a valid-credential RDP session from Kali. Windows recorded **Security 4624** Logon Type 3 followed by Type 10 (RemoteInteractive).
5. **PowerShell execution:** From the RDP session, launched a child PowerShell command to create `C:\LabArtifacts\LAB004-RDP-session.txt`; correlated **Sysmon 1** and **Sysmon 11**.
6. **Benign persistence:** Created `LAB004-Persistence`, a scheduled task configured to run at user logon. The first task action referenced a misspelled directory (`C:\LabArtifaacts\`) and did not produce the intended marker. Modified the action to use `C:\LabArtifacts\`, manually ran the task, and confirmed the marker file `LAB004-task.txt` with `LAB004-task-executed` content.
7. **Timeline analysis:** Correlated RDP, PowerShell, scheduled-task creation, task execution, and file-creation signals in Splunk; recorded process parent/child relationships.
8. **Acquisition:** Exported `Security` and `Microsoft-Windows-Sysmon/Operational` event logs with `wevtutil epl` into native `.evtx` files. Calculated SHA-256 hashes before transfer, copied through a VirtualBox shared folder to the removable USB, and confirmed identical hashes with Linux `sha256sum`.

## Key event timeline

| Local time (PDT), 2026-10-19 | Source | Observed activity |
| --- | --- | --- |
| 15:03:18.550 | Security 4625 | Failed network authentication to account `dylan` from Kali `192.168.56.102` (NTLM; Logon Type 3) |
| 15:36:59.954 | Security 4624 | Successful network authentication from Kali (Type 3) |
| 15:37:01.840 | Security 4624 | Successful RDP remote interactive login (Type 10); duplicate search row is **not** counted as a separate session |
| 15:50:50.536 | Sysmon 1 | PowerShell child process created `LAB004-RDP-session.txt` using `Set-Content` |
| 15:50:51.038 | Sysmon 11 | File-creation record for `LAB004-RDP-session.txt` |
| 15:58:12.110 | Sysmon 1 | `schtasks.exe /Create` for `LAB004-Persistence`, originally referencing `LabArtifaacts` |
| 16:01:27.822 | Sysmon 1 | First `schtasks.exe /Run` attempt |
| 16:01:27.864 | Sysmon 1 | Scheduler-launched `cmd.exe` with incorrect output path, parent `svchost.exe` |
| 16:15:50.672 | Sysmon 1 | `schtasks.exe /Change` corrected the output directory |
| 16:16:45.952 | Sysmon 1 | Second `schtasks.exe /Run` attempt |
| 16:16:46.002 | Sysmon 1 | `cmd.exe` started by Task Scheduler, parent `svchost.exe`, with corrected output path |
| 16:16:47.040 | Sysmon 11 | File-creation event observed in the run window (path not populated in the shared Splunk table); marker content separately verified on Windows |

## Findings

1. **Authentication correlation:** Windows Security event 4625 recorded the initial failed authentication from `192.168.56.102`; later event 4624, Logon Type 10, confirmed authorized RDP access from that IP.
2. **Process execution evidence:** Sysmon event 1 documented PowerShell execution and the use of `schtasks.exe`. Sysmon event 11 documented creation of the remote-session test artifact.
3. **Persistence mechanism:** `LAB004-Persistence` was an **actual Windows scheduled task** with a benign logon-triggered action. Task Scheduler launched its action through `cmd.exe` with parent `svchost.exe`. The corrected action successfully produced its intended file.
4. **Investigative nuance:** The first task execution failure was attributable to a misspelled path, not a failure of scheduling. Investigation relied on recorded process command lines rather than assumptions.
5. **No compromise claim:** The activity was operator-controlled; there was no evidence of credential theft, exploit-based entry, malicious payload, or unauthorized persistence.

## MITRE ATT&CK context

| Technique | ID | Lab representation |
| --- | --- | --- |
| Remote Services: Remote Desktop Protocol | **T1021.001** | Connection over RDP from Kali to Windows (authorized demonstration; not lateral movement across compromised hosts) |
| Command and Scripting Interpreter: PowerShell | **T1059.001** | Child PowerShell process creating a benign artifact |
| Scheduled Task/Job: Scheduled Task | **T1053.005** | `schtasks.exe` registration and manual execution of a logon-triggered task |

These are **behavioral mappings**, not assertions of adversarial intent or complete emulation of every technique.

## Evidence acquisition and integrity

Original-format logs were exported from the Windows VM and preserved under `DFIR-LAB004/evidence/originals/` on removable USB. The hash manifest resides in `DFIR-LAB004/hashes/`. Hashes were recomputed from the USB copies and matched those recorded at acquisition.

| Evidence file | SHA-256 |
| --- | --- |
| `LAB004-Security.evtx` | `1b284fabd519f2366a004af344b91ddc82d0566dc279764ccdda2869010c1f34` |
| `LAB004-Sysmon.evtx` | `969be0b15e5160918968f397c9fa3c48c54204153beb49a11f0c6c080864b0f2` |

**Handling boundary:** SHA-256 agreement establishes that the transferred copies match the exports that were hashed; it does **not** independently prove the events' origin or that the live Windows logs were immutable before export. Raw event logs and the full USB manifest are intentionally not committed to this public repository.

## Investigation report

See [`reports/investigation-report.md`](reports/investigation-report.md) for narrative analysis, security interpretation, limitations, and cleanup checklist.

## Conclusion

This lab demonstrates hands-on Windows event-log collection, Sysmon-based process and file activity analysis, SIEM correlation, RDP forensic interpretation, ATT&CK-aligned persistence emulation, and integrity-verified evidence transfer. The observed behaviors are accurately described as **authorized simulation**, not professional incident response work or evidence of a real attacker.
