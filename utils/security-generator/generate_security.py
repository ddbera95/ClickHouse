#!/usr/bin/env python3
from pathlib import Path
from typing import List

VERSIONS_FILE = (
    Path(__file__).absolute().parent.parent / "list-versions" / "version_date.tsv"
)

HEADER = """<!--
the file is autogenerated by utils/security-generator/generate_security.py
-->

# Security Policy

## Security Announcements
Security fixes will be announced by posting them in the [security changelog](https://clickhouse.com/docs/en/whats-new/security-changelog/).

## Scope and Supported Versions

The following versions of ClickHouse server are currently being supported with security updates:
"""

FOOTER = """## Reporting a Vulnerability

We're extremely grateful for security researchers and users that report vulnerabilities to the ClickHouse Open Source Community. All reports are thoroughly investigated by developers.

To report a potential vulnerability in ClickHouse please send the details about it to [security@clickhouse.com](mailto:security@clickhouse.com). We do not offer any financial rewards for reporting issues to us using this method. Alternatively, you can also submit your findings through our public bug bounty program hosted by [Bugcrowd](https://bugcrowd.com/clickhouse) and be rewarded for it as per the program scope and rules of engagement.

### When Should I Report a Vulnerability?

- You think you discovered a potential security vulnerability in ClickHouse
- You are unsure how a vulnerability affects ClickHouse

### When Should I NOT Report a Vulnerability?

- You need help tuning ClickHouse components for security
- You need help applying security related updates
- Your issue is not security related

## Security Vulnerability Response

Each report is acknowledged and analyzed by ClickHouse maintainers within 5 working days.
As the security issue moves from triage, to identified fix, to release planning we will keep the reporter updated.

## Public Disclosure Timing

A public disclosure date is negotiated by the ClickHouse maintainers and the bug submitter. We prefer to fully disclose the bug as soon as possible once a user mitigation is available. It is reasonable to delay disclosure when the bug or the fix is not yet fully understood, the solution is not well-tested, or for vendor coordination. The timeframe for disclosure is from immediate (especially if it's already publicly known) to 90 days. For a vulnerability with a straightforward mitigation, we expect the report date to disclosure date to be on the order of 7 days.
"""


def generate_supported_versions():
    with open(VERSIONS_FILE, "r", encoding="utf-8") as fd:
        versions = [line.split(maxsplit=1)[0][1:] for line in fd.readlines()]


    # The versions in VERSIONS_FILE are ordered ascending, so the first one is
    # the greatest one. We may have supported versions in the previous year
    unsupported_year = int(versions[0].split(".", maxsplit=1)[0]) - 2
    # 3 supported versions
    supported = []  # type: List[str]
    # 2 LTS versions, one of them could be in supported
    lts = []  # type: List[str]
    # The rest are unsupported
    unsupported = []  # type: List[str]
    table = [
        "| Version | Supported |",
        "|:-|:-|",
    ]
    for version in versions:
        year = int(version.split(".")[0])
        month = int(version.split(".")[1])
        version = f"{year}.{month}"
        if version in supported or version in lts:
            continue
        if len(supported) < 3:
            supported.append(version)
            if len(lts) < 2 and month in [3, 8]:
                # The version can be LTS as well
                lts.append(version)
            table.append(f"| {version} | ✔️ |")
            continue
        if len(lts) < 2 and month in [3, 8]:
            lts.append(version)
            table.append(f"| {version} | ✔️ |")
            continue
        if year <= unsupported_year:
            # The whole year is unsupported
            version = f"{year}.*"
        if not version in unsupported:
            unsupported.append(version)
            table.append(f"| {version} | ❌ |")

    return "\n".join(table) + "\n"


def main():
    print(HEADER)
    print(generate_supported_versions())
    print(FOOTER)


if __name__ == "__main__":
    main()
