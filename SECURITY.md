# Security Policy

## Security Advisories

Security advisories are documented using the Vulnerability Exploitability eXchange (VEX) standard. This project maintains VEX source files in YAML and uses them to generate OpenVEX documents that are consumed by a dependency vulnerability scanner.

Each advisory identifies the vulnerability being assessed, the associated product (e.g., Python package), its current status (one of `not_affected`, `affected`, `fixed`, or `under_investigation`), and the rationale supporting that status. When a vulnerability is determined to be `not_affected`, the advisory includes a justification and an impact statement describing why we believe the vulnerability is not exploitable within the context of this project.

For information about the latest security advisories for this project, please refer to the following:
* [{{ cookiecutter.project_slug }}/src/vex.yaml]({{%20cookiecutter.project_slug%20}}/src/vex.yaml)

## Reporting a Vulnerability

To report a security issue, please use https://github.com/orgs/deathlabs/discussions/new?category=security. We will do our best to respond to reports within 7 business days.
