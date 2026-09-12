# Security policy

## Scope

Report vulnerabilities in the validator, unsafe parsing behavior, accidental execution of retrieved content, or ways the project could cause private data to enter a public record.

## Out of scope

The project does not fetch URLs, execute source content, manage credentials, or promise that a claim is true. Do not submit real secrets, private logs, personal data, or infrastructure details in Issues or fixtures.

## Reporting

For a suspected private-data exposure or credential leak, do not open a public Issue. Contact the maintainer through a private GitHub security channel if one is available. Otherwise, report only that a private report is needed and omit the sensitive payload.

## Maintainer rules

- Do not request server, workspace, token, or Actions-secret access from contributors.
- Prefer a minimal reproducer using synthetic data.
- Fix public exposure promptly and document the preventive rule.

