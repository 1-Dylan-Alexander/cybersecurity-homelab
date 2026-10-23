# Evidence, Ethics, and Publication Standards

[← Portfolio home](../README.md) · [Implemented architecture](architecture.md)

These standards apply to the public **cybersecurity-homelab** repository. They describe how lab results are represented and what is safe to publish; they do **not** imply the presence of a formal corporate evidence-management program.

## Scope and authorization

All scanning, authentication tests, endpoint telemetry generation, and persistence emulation described in these projects were performed in an isolated, authorized personal environment. Lab exercises are never labeled as real-world compromises.

## What public artifacts can demonstrate

- Commands, search logic, and configurations can show **methodology**.
- Sanitized results and investigation reports can show **observations and reasoning**.
- Technical findings should identify the corresponding **source event, command output, or artifact**.
- Conclusions must state material **uncertainty and investigative limitations**.

## What stays private

Do not commit credentials, tokens, private keys, unredacted user-related logs, sensitive network captures, or unsanitized screenshots. Original Windows `.evtx` exports for LAB-004 and the USB hash manifest stay on private removable media, not in this repository.

The [repository .gitignore](../.gitignore) excludes common secrets, VM images, crash dumps, and native Windows event-log export formats. Ignore rules alone cannot guarantee protection; **review staged changes before every push**.

## Reproducibility and evidence integrity

Record, when available, the source system, collection method, timestamps/time zone, tool/version, scope, and observed outcomes. If copies are hashed, identify the algorithm and the point in the workflow when each hash was recorded.

**LAB-004 boundary:** SHA-256 agreement between the Windows-side baseline and transferred copies establishes byte-level agreement with the hashed exports. It does not establish that live event logs were immutable prior to export or provide a complete legal chain of custody. The USB is not claimed to be write-once storage.

## Reporting discipline

Use **observed**, **consistent with**, **potential**, **not established**, and **confirmed** with care. Examples:

- An FTP software version associated with a CVE is **not proof** that a vulnerability was exploitable.
- One failed RDP authentication is **not proof** of password spraying or brute force.
- An authorized scheduled task can model a persistence technique without establishing malicious persistence.
- An event correlated by timestamp is weaker evidence of file-path identity than an event showing the target filename.

## Adding future lab evidence

Before publication:

1. Check the artifact for credentials, usernames, session material, public IPs, customer data, and other unnecessary identifiers.
2. Sanitize or redact where appropriate, and disclose material redactions that affect interpretation.
3. Link the artifact from the corresponding LAB-NNN README.
4. Document what it supports and any important gaps. Never fabricate log lines, timestamps, outcomes, screenshots, or chain-of-custody fields.

All completed labs are listed in the [main portfolio README](../README.md).
