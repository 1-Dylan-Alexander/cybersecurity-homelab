# LAB-004 — DFIR Incident Investigation Report

**Case identifier:** LAB-004  
**Case type:** Controlled Windows RDP intrusion / scheduled-task persistence simulation  
**Date:** October 19, 2026 (local timestamps in PDT)  
**Case status:** Simulated activity completed; central log investigation and copied-evidence hash verification completed  
**Severity:** *N/A — authorized lab simulation*  
**Evidence classification:** Original-format `.evtx` exports stored on private removable media; this report contains derived metadata only

## Executive summary

A simulated originating host (Kali Linux, `192.168.56.102`) connected to an isolated Windows 11 Enterprise VM (`192.168.56.104`). A FreeRDP authentication request failed at 15:03:18 and was logged as Windows Security event 4625. A later authorized login succeeded at approximately 15:37, producing Security event 4624 with Logon Types 3 and 10. From the remote session, a PowerShell process created a marker file. The operator then created and executed a benign scheduled task configured to run at logon. An initial typo in the task's output path prevented the intended marker; after correcting the path, the task executed and created the marker.

Splunk Enterprise correlated Windows authentication events and Sysmon process/file telemetry into a single timeline. Native event-log exports were SHA-256 hashed, transferred to a dedicated USB, and verified after transfer. **No unauthorized access, malware execution, credential theft, or actual compromise was observed or claimed.**

## Scope and system details

- Windows endpoint: `DESKTOP-TH2SL52`, Windows 11 Enterprise Evaluation, `192.168.56.104`
- Simulated source: Kali Linux VM, `192.168.56.102`
- SIEM receiver: Linux Mint host, Splunk Enterprise 10.6.0.5, `192.168.56.1:9997`
- Network: VirtualBox host-only `192.168.56.0/24`, with Windows RDP firewall restrictions to the Kali IP
- Telemetry: Windows Security event log and Sysmon Operational log forwarded via Splunk Universal Forwarder
- Scope: Single Windows VM and operator-controlled traffic only; no real victim, compromised user, or external adversary
- Baseline VirtualBox snapshot: `LAB004-BASELINE-PRE-ATTACK`

## Evidence sources

| ID | Source | Main fields used |
| --- | --- | --- |
| E01 | Windows Security exported event log | `EventCode`, account, source network address, logon type, status/substatus, timestamp |
| E02 | Windows Sysmon exported Operational log | Event ID, `Image`, `CommandLine`, `ParentImage`, `TargetFilename`, timestamp |
| E03 | Splunk correlation results | Filtered and chronologically ordered Security/Sysmon events |
| E04 | Benign Windows marker files | Operator-confirmed file output after PowerShell / scheduled-task tests |
| E05 | Original and post-transfer SHA-256 hashes | Evidence-copy integrity comparison |

## Timeline

| Time (PDT) | Event | Interpretation |
| --- | --- | --- |
| 15:03:18.550 | Security 4625, `dylan`, Type 3, source `192.168.56.102`, `0xC000006D/0xC000006A` | Network logon rejected because supplied credentials were invalid. FreeRDP proceeded without the operator manually supplying an incorrect password; exact submitted credential material is unknown. |
| 15:36:59.954 | Security 4624, `dylan`, Type 3, source `192.168.56.102` | Successful initial network authentication |
| 15:37:01.840 | Security 4624, `dylan`, Type 10, source `192.168.56.102` | Successful remote interactive RDP login; duplicated output row not counted as a distinct session |
| 15:50:50.536 | Sysmon 1, `powershell.exe` | Child PowerShell started with `-NoProfile` and `Set-Content` command targeting `C:\LabArtifacts\LAB004-RDP-session.txt` |
| 15:50:51.038 | Sysmon 11, `powershell.exe` | Creation of `C:\LabArtifacts\LAB004-RDP-session.txt` |
| 15:58:12.110 | Sysmon 1, `schtasks.exe /Create` | Logon-triggered scheduled task `LAB004-Persistence` registered with misspelled output directory `LabArtifaacts` |
| 16:01:27.822–16:01:27.879 | Sysmon 1, `schtasks.exe`, `cmd.exe`, `conhost.exe` | Manual run requested; task action launched through Scheduler; marker absent from correct directory because action referenced typo path |
| 16:15:50.672 | Sysmon 1, `schtasks.exe /Change` | Task action updated to correct directory `C:\LabArtifacts\` |
| 16:16:45.952–16:16:46.013 | Sysmon 1, `schtasks.exe`, `cmd.exe`, `conhost.exe` | Corrected task manually triggered and action process launched, with `cmd.exe` parent `svchost.exe` |
| 16:16:47.040 | Sysmon 11 | File creation observed after action execution; `TargetFilename` not visible in supplied Splunk table |

### Relevant event interpretation

**Security Event 4625:** NTLM authentication failed for `DESKTOP-TH2SL52\dylan` from `192.168.56.102`, Logon Type 3. `0xC000006D` denotes logon failure; `0xC000006A` indicates an incorrect password. This record proves a failed logon, **not** manual bad-password entry, password spraying, or brute force.

**Security Event 4624:** Logon Type 3 documented network authentication; subsequent Type 10 provided strong evidence of an established RDP remote-interactive session. Repeated search rows at the same instant were not treated as independent sessions.

**Sysmon Event 1:** Detailed command lines supplied high-quality evidence for the PowerShell marker and scheduled-task lifecycle. The `cmd.exe` process launched for the task had `svchost.exe` as its parent, consistent with Task Scheduler service execution. The first task action contained a path typo; this was found directly in the recorded `CommandLine` and corrected.

**Sysmon Event 11:** Confirmed creation of the PowerShell marker. Another event appeared after the corrected task launched, but the supplied table did not populate `TargetFilename`; the operator separately verified the intended `LAB004-task.txt` marker content on Windows. The latter event is correlated by time, rather than claimed as direct file-path proof.

## MITRE ATT&CK behavioral alignment

- **T1021.001 — Remote Services: Remote Desktop Protocol:** An authorized session used RDP. This is a protocol/behavior mapping, not evidence of lateral movement in a compromised network.
- **T1059.001 — Command and Scripting Interpreter: PowerShell:** Remote session launched PowerShell and wrote a benign marker.
- **T1053.005 — Scheduled Task/Job: Scheduled Task:** A Windows logon-triggered scheduled task was created, modified, and manually executed using `schtasks.exe`.

## Preservation methodology and SHA-256 integrity

1. Used `wevtutil epl Security` to export Windows Security to `LAB004-Security.evtx`.
2. Used `wevtutil epl "Microsoft-Windows-Sysmon/Operational"` to export Sysmon Operational to `LAB004-Sysmon.evtx`.
3. Computed file SHA-256 hashes in Windows with `Get-FileHash -Algorithm SHA256`; saved results in `LAB004-SHA256.txt`.
4. Copied both exports and hash manifest via a temporary VirtualBox shared folder to Linux Mint.
5. Copied `.evtx` exports to the USB directory `evidence/originals/` and manifest to `hashes/` on exFAT volume `DFIR-LAB004`.
6. Recomputed SHA-256 hashes on the USB using `sha256sum`; both matched the Windows-side values.

| SHA-256 verification | Hash |
| --- | --- |
| `LAB004-Security.evtx` | `1b284fabd519f2366a004af344b91ddc82d0566dc279764ccdda2869010c1f34` |
| `LAB004-Sysmon.evtx` | `969be0b15e5160918968f397c9fa3c48c54204153beb49a11f0c6c080864b0f2` |

**Caveats:** Acquired files are event-log **exports**, not a full forensic disk image. Hash equality verifies byte-level consistency between the hash baseline and copied exports, but does not prove pre-export immutability of the live log. The evidence USB is exFAT and not represented as WORM media. Detailed chain-of-custody timestamps and named custody transfers were not recorded and are not fabricated in this report.

## Assessment and outcome

**Outcome:** The sequence was reconstructed using SIEM and endpoint telemetry. The task lifecycle was distinguishable from benign interactive actions through command lines, timestamps, and parent-child process relations. The Windows evidence exports were acquired in native format and integrity-verified after transfer to dedicated removable storage.

**Analytical confidence:** High for presence of the specific logon events and recorded commands; moderate for associating the final Sysmon Event 11 with the intended task marker because the supplied Splunk table omitted its path. No attribution beyond the known lab operator and authorized simulated source.

## Cleanup checklist (perform after preserving evidence)

- [ ] Delete benign scheduled task after evidence acquisition: `schtasks.exe /Delete /TN "LAB004-Persistence" /F` (Windows Administrator PowerShell).
- [ ] Confirm task removal with `Get-ScheduledTask -TaskName 'LAB004-Persistence'` (expect not found).
- [ ] Optionally remove benign markers after capturing any final screenshots or metadata needed for documentation.
- [ ] Remove the temporary VirtualBox shared-folder mapping and transfer staging files after confirming USB evidence copies, if no longer needed.
- [ ] Safely unmount/eject `DFIR-LAB004` after all writes finish; retain original-format exports privately.
- [ ] Restore the VM's pre-simulation snapshot **only if** the current state and any remaining evidence are no longer needed; snapshot restoration would discard later state.

## Final determination

**Controlled authorized simulation completed.** Authentication and post-login activity were detected and correlated in Splunk, and preserved Windows evidence exports matched their original hashes after copying. This lab demonstrates practical blue-team investigation and DFIR evidence-handling skills; it is not a record of professional production incident response or a real compromise.
