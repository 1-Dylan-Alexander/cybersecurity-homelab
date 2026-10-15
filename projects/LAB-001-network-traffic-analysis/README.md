# Network Traffic Analysis — Lab 01

## Overview
This blue-team lab introduces network packet capture, traffic filtering, and baseline analysis using tcpdump. It builds on the existing VSFTPD 2.3.4 vulnerability assessment in the cybersecurity-homelab repository.

## Objectives
- Identify network capture interfaces.
- Capture and interpret ICMP traffic.
- Investigate UDP broadcast activity.
- Apply Berkeley Packet Filter (BPF) expressions.
- Document findings using an evidence-based SOC workflow.

## Lab Environment
| Component | Configuration |
|---|---|
| Host | Linux Mint 22.3, ThinkPad T480 |
| Hypervisor | VirtualBox |
| Analyst VM | Kali Linux — 192.168.56.102 |
| Target VM | Metasploitable 2 — 192.168.56.103 |
| Network | Host-only, 192.168.56.0/24 |
| Capture interface | Kali eth0 |
| tcpdump | 4.99.4 (verified on Linux Mint host) |
| libpcap | 1.10.4 (verified on Linux Mint host) |

## Commands Used
```bash
# Inspect interfaces on Kali
ip -br addr

# Verify communication with Metasploitable
ping -c 4 192.168.56.103

# Capture 10 packets
sudo tcpdump -i eth0 -nn -c 10

# Filter UDP port 137 traffic
sudo tcpdump -i eth0 -nn -c 5 'udp port 137'

# Attempt verbose protocol inspection
sudo tcpdump -i eth0 -nn -vv -c 5 'udp port 137'
```

## Findings

### Finding 01 — ICMP Connectivity
Kali sent four ICMP Echo Requests to Metasploitable and received four replies, with zero packet loss and an average round-trip time of 1.256 ms.

The initial tcpdump capture recorded three Echo Request/Reply pairs. Its 10-packet capture limit was reached before the fourth pair could be recorded.

**Assessment:** Expected connectivity-testing traffic; no suspicious activity identified.

### Finding 02 — UDP Port 137 Broadcasts
Metasploitable transmitted UDP packets from 192.168.56.103:137 to 192.168.56.255:137, the subnet broadcast address.

A filtered capture recorded five packets, with UDP payload lengths of 50 and 68 bytes. The behavior persisted after restarting Metasploitable.

UDP port 137 is commonly used by NetBIOS Name Service (NBNS). The observed broadcasts are consistent with name-resolution or name-registration activity, but packet contents were not decoded to confirm their precise purpose.

**Assessment:** Likely background NetBIOS-related traffic. No malicious behavior established.

### Finding 03 — Capture Statistics
The initial general capture and subsequent filtered capture each recorded 0 packets dropped by the kernel. This does not prove that all network traffic was observed.

## Limitations
- No PCAP file was saved.
- No Wireshark analysis was performed.
- Detailed NBNS message contents were not decoded.
- The tcpdump version was verified on the Linux Mint host, not separately inside Kali.
- No intrusion or exploitation attempt was analyzed.

## SOC Skills Practiced
- Capture-interface identification
- ICMP traffic interpretation
- UDP broadcast identification
- BPF capture filtering
- Basic network baselining
- Separating observed facts from hypotheses
- Documenting investigation limitations

## Conclusion
This lab established an initial network traffic baseline for the isolated Kali–Metasploitable environment. Traffic analysis confirmed successful ICMP connectivity and recurring UDP port 137 broadcasts. Neither observation alone established malicious activity.

## Next Steps
1. Verify Wireshark installation in Kali.
2. Capture and preserve PCAP evidence.
3. Decode NBNS traffic using Wireshark.
4. Analyze TCP handshakes and FTP traffic.
5. Correlate packet evidence with the existing VSFTPD 2.3.4 vulnerability assessment.

## Related Work
Repository: https://github.com/1-Dylan-Alexander/cybersecurity-homelab

Previous project: VSFTPD 2.3.4 vulnerability assessment.
