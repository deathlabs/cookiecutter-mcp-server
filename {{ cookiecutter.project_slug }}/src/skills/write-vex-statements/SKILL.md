---
name: write-vex-statements
description: Draft, review, and refine evidence-backed OpenVEX vulnerability statements in YAML or JSON. Use when assessing a CVE or GHSA finding, choosing a VEX status or justification, matching a product PURL to an SBOM component, writing an impact statement, updating a vex.yaml file, or deciding whether a scanner finding can be suppressed.
---

# Write VEX Statements

Produce concise VEX statements that reflect the installed product and the actual exploit path. Treat VEX as a security assertion supported by evidence, not merely as a way to suppress a scanner finding.

## Workflow

1. Identify the advisory and affected package ecosystem.
2. Verify the affected and fixed version ranges from an authoritative advisory.
3. Identify the exact installed component from the SBOM, lockfile, or built image.
4. Confirm that the finding applies to that component and version.
5. Inspect the application and relevant dependencies for the vulnerable behavior.
6. Select the appropriate status and justification.
7. Write an impact statement describing the decisive technical facts.
8. Match every product PURL exactly to the SBOM.
9. Return an insertion-ready VEX statement and identify any unverified assumptions.

Do not conclude that a product is `not_affected` solely because the application lacks a direct import or function call. Account for frameworks, plugins, and transitive dependencies that could invoke the vulnerable code.

## Select a Status

Use one of the following statuses:

- `not_affected`: Evidence establishes that the vulnerability cannot affect the listed product in its deployed context.
- `fixed`: The listed product version contains the remediation.
- `affected`: The vulnerable condition is reachable, or exposure cannot reasonably be excluded.
- `under_investigation`: Material facts remain unresolved.

Do not describe an affected package version as `fixed`. Do not describe a patched version as `not_affected` merely because the vulnerable path is unused.

## Select a Justification

For `not_affected`, choose the narrowest justification supported by the evidence:

- `component_not_present`: The affected component is absent from the product.
- `vulnerable_code_not_present`: The component is present, but the vulnerable code is absent, removed, or not compiled into it.
- `vulnerable_code_not_in_execute_path`: The vulnerable code exists, but no deployed execution path reaches it.
- `vulnerable_code_cannot_be_controlled_by_adversary`: The code executes, but an adversary cannot influence the required input or state.
- `inline_mitigations_already_exist`: Existing controls in the execution path prevent exploitation.

Do not include a `not_affected` justification with `fixed`, `affected`, or `under_investigation` unless the project’s local schema explicitly requires it.

## Write the Impact Statement

Write one or two sentences that:

1. Explain why the affected component or code is present when useful.
2. Name the vulnerable function, feature, protocol, configuration, or input condition.
3. Explain why that condition is absent, unreachable, or not adversary-controlled.

Prefer specific statements:

```text
The cryptography package is installed, but this service does not call the
pkcs7_decrypt_der(), pkcs7_decrypt_pem(), or pkcs7_decrypt_smime() functions
or decrypt attacker-supplied PKCS#7 EnvelopedData.
```
