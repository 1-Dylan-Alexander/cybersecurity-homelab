# Cybersecurity Homelab Architecture

## Purpose

This document defines the technical architecture of the cybersecurity homelab.

The environment is designed to provide an isolated, resource-conscious environment for practicing defensive security concepts, system hardening, network security, security monitoring, centralized logging, investigation, and incident response.

## Host Environment

| Component | Specification |
|---|---|
| Host | Lenovo ThinkPad T480 |
| CPU | Intel Core i5-8250U |
| Memory | 16 GB RAM |
| Architecture | x86_64 |
| Host OS | Linux Mint |
| Hypervisor | VirtualBox |

## Architecture Principles

The lab will be designed around the following principles:

- Network segmentation
- Isolation between the host and lab environment
- Dedicated management access
- Controlled communication between systems
- System hardening
- Least privilege
- Centralized security logging
- Security monitoring
- Reproducible configuration
- Evidence collection
- Documented investigation workflows

## Logical Architecture

```text
                         INTERNET
                            |
                            |
                    +-------v-------+
                    |    Gateway    |
                    | / Firewall    |
                    +-------+-------+
                            |
                    +-------v-------+
                    | Lab Network   |
                    +-------+-------+
                            |
              +-------------+-------------+
              |                           |
      +-------v-------+           +-------v-------+
      | Management    |           | Lab Systems   |
      | Zone          |           | Zone          |
      +-------+-------+           +-------+-------+
              |                           |
        +-----v-----+              +------+------+
        | Admin     |              | Endpoints / |
        | System    |              | Servers     |
        +-----------+              +------+------+
                                         |
                                  +------v------+
                                  | Monitoring  |
                                  | / SIEM      |
                                  +-------------+
