# Cybersecurity Homelab

## Overview

This repository documents the development of a hands-on cybersecurity homelab focused on building practical **Blue Team, Security Operations Center (SOC), network security, and vulnerability management skills**.

The homelab supports my preparation for the CompTIA Security+ certification and my professional development toward entry-level IT support and SOC analyst roles.

The environment is built around a Lenovo ThinkPad T480 running Linux Mint 22.3, with Oracle VirtualBox providing isolated virtual networks for security testing, traffic analysis, vulnerability assessment, and defensive monitoring.

Each project emphasizes technical understanding, reproducible procedures, evidence collection, and professional documentation.

## Objectives

- Develop practical Blue Team and defensive security skills.
- Reinforce CompTIA Security+ concepts through hands-on exercises.
- Practice network traffic analysis and protocol investigation.
- Identify vulnerabilities and evaluate security risks.
- Develop foundational threat detection and incident response skills.
- Configure and evaluate security monitoring tools.
- Practice Linux administration and system hardening.
- Collect, preserve, and analyze security evidence.
- Develop technical reporting and investigation documentation.
- Maintain a professional GitHub portfolio demonstrating measurable progress.

## Lab Environment

### Host System

| Component | Specification |
|---|---|
| Computer | Lenovo ThinkPad T480 |
| Operating System | Linux Mint 22.3 |
| Processor | Intel Core i5-8250U |
| Memory | 16 GB DDR4 |
| Architecture | x86_64 |
| Virtualization | Oracle VirtualBox |
| Version Control | Git |
| Repository Hosting | GitHub |

### Virtual Machines

| Virtual Machine | IP Address | Purpose |
|---|---|---|
| Kali Linux | 192.168.56.102 | Security testing, packet analysis, network investigation |
| Metasploitable 2 | 192.168.56.103 | Intentionally vulnerable target for authorized security assessments |

### Network Architecture

The laboratory uses a VirtualBox host-only network to isolate security testing from external networks.

- **Network:** 192.168.56.0/24
- **Host-only interface:** vboxnet0
- **Kali interface:** eth0
- **Metasploitable interface:** Host-only adapter
- **Internet connectivity:** Separate NAT adapter on Kali

All vulnerability assessments and controlled security testing are performed against authorized systems within the laboratory environment.

## Cybersecurity Labs

All cybersecurity labs use a single sequential numbering system regardless of specialization.

Each lab follows a standardized documentation format covering objectives, tools, procedures, evidence, findings, and conclusions.

| Lab ID | Project | Specialization | Status |
|---|---|---|---|
| LAB-001 | [Network Traffic Analysis with tcpdump](projects/LAB-001-network-traffic-analysis/README.md) | Blue Team / Network Security | Documented |
| LAB-002 | [VSFTPD 2.3.4 Vulnerability Assessment](projects/LAB-002-vsftpd-vulnerability-assessment/README.md) | Vulnerability Assessment | Documented |

### LAB-001 — Network Traffic Analysis with tcpdump

**Focus:** Network Security Monitoring and Packet Analysis

This lab introduces command-line packet capture using tcpdump in an isolated virtual network.

**Skills demonstrated:**

- Identifying Linux network interfaces.
- Capturing network packets using tcpdump.
- Analyzing ICMP Echo Requests and Replies.
- Identifying UDP broadcast traffic.
- Applying Berkeley Packet Filter (BPF) expressions.
- Investigating NetBIOS-related traffic on UDP port 137.
- Establishing baseline network behavior.
- Documenting observations and investigation limitations.

**Findings:** Successful ICMP connectivity between Kali and Metasploitable was confirmed. Recurring UDP port 137 broadcasts were observed. No malicious behavior was confirmed.

**Status:** Introductory packet analysis documented. Wireshark inspection and saved PCAP evidence remain future work.

[View LAB-001 Documentation](projects/LAB-001-network-traffic-analysis/README.md)

### LAB-002 — VSFTPD 2.3.4 Vulnerability Assessment

**Focus:** Service Enumeration, Vulnerability Identification, and Risk Assessment

This lab examines the FTP service running on Metasploitable 2 and investigates its association with CVE-2011-2523.

**Skills demonstrated:**

- Service enumeration using Nmap.
- Software and version identification.
- FTP service analysis.
- Researching known vulnerabilities.
- Understanding CVE identifiers.
- Evaluating potentially vulnerable services.
- Developing remediation recommendations.
- Documenting vulnerability assessment findings.

**Findings:** Nmap identified vsftpd 2.3.4 running on TCP port 21. The service version is associated with CVE-2011-2523, but exploitation was not performed and the presence of the backdoor was not confirmed.

**Status:** Vulnerability assessment documented.

[View LAB-002 Documentation](projects/LAB-002-vsftpd-vulnerability-assessment/README.md)

## Tools and Technologies

The homelab incorporates tools for network investigation, vulnerability analysis, intrusion detection, and system administration.

| Tool | Primary Purpose |
|---|---|
| Linux Mint | Host operating system |
| Kali Linux | Security assessment and investigation environment |
| VirtualBox | Virtual machine and network isolation |
| tcpdump | Network packet capture |
| Wireshark | Packet inspection and protocol analysis |
| Nmap | Network and service enumeration |
| Snort | Network intrusion detection |
| Nessus | Vulnerability scanning |
| Metasploit Framework | Authorized vulnerability validation |
| Git | Version control |
| GitHub | Documentation and portfolio management |

Tool installation and availability do not imply that each tool has been fully exercised in a published lab.

## Repository Structure

```text
cybersecurity-homelab/
├── README.md
├── .gitignore
├── docs/
│   └── architecture.md
├── infrastructure/
│   ├── virtual-machines/
│   └── networking/
├── projects/
│   ├── LAB-001-network-traffic-analysis/
│   │   └── README.md
│   └── LAB-002-vsftpd-vulnerability-assessment/
│       └── README.md
├── evidence/
│   ├── logs/
│   ├── reports/
│   │   └── vsftpd/
│   │       ├── ftp-enumeration.txt
│   │       └── report.md
│   └── screenshots/
├── scripts/
└── notes/
```

Some infrastructure and evidence directories are reserved for future projects and may not yet contain tracked files.

## Lab Documentation Standards

Every completed lab should include the following sections:

1. **Objectives** — What the exercise aims to accomplish.
2. **Tools and Environment** — Software, hardware, network configuration, and relevant versions.
3. **Procedures** — Commands, configurations, and investigative methodology.
4. **Evidence** — Supporting logs, packet captures, screenshots, and technical reports.
5. **Findings** — Verified observations and their security implications.
6. **Conclusions** — Results, limitations, lessons learned, and recommended next steps.

Lab documentation must distinguish between confirmed security findings, potential vulnerabilities, and hypotheses requiring further investigation.

## Evidence Management

Evidence is organized to support reproducibility and technical review.

Examples include:

- Nmap scan results.
- Network packet captures (PCAP).
- Intrusion detection alerts.
- Vulnerability scan reports.
- Linux system and authentication logs.
- Configuration files.
- Terminal screenshots.

Sensitive information, credentials, private keys, and unrelated network traffic should not be committed to the repository.

## Professional Development Goals

This homelab supports continued progression in:

- Linux system administration.
- TCP/IP networking fundamentals.
- Network Security Monitoring (NSM).
- Security Information and Event Management (SIEM).
- Intrusion Detection Systems (IDS).
- Vulnerability management.
- Security event investigation.
- Incident response fundamentals.
- Security automation and scripting.
- Technical communication and reporting.

Future exercises will emphasize the detection, analysis, and documentation skills used by entry-level SOC analysts.

## Documentation Philosophy

The purpose of this repository is not simply to demonstrate the execution of cybersecurity tools.

Each lab is intended to demonstrate an understanding of:

- Why a tool or technique was selected.
- How the technology operates.
- What the collected evidence actually demonstrates.
- How findings relate to security risks.
- What limitations affect the conclusions.
- How the results can be communicated professionally.

The long-term objective is to develop a practical, evidence-based cybersecurity portfolio that demonstrates continued technical growth and readiness for entry-level defensive security responsibilities.

---

**Repository:** [1-Dylan-Alexander/cybersecurity-homelab](https://github.com/1-Dylan-Alexander/cybersecurity-homelab)

**Primary Focus:** Blue Team Security | SOC Analysis | Network Security | Vulnerability Management
