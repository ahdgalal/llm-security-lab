# Security Scan Decisions

Last updated: 2026-10-12

## CI failure policy

| Check | When CI fails | Reason |
|---|---|---|
| Bandit | A security finding is reported in application code | Prevent known insecure coding patterns from passing unnoticed. |
| pip-audit | A known vulnerability is found in the locked dependencies | Keep vulnerable dependencies from passing silently. |
| Docker image secrets | A potential secret is detected | Investigate before shipping a possible credential leak. |
| Dockerfile configuration | A High or Critical misconfiguration is found | Block serious insecure container configurations. |
| Image vulnerabilities | A fixable High or Critical vulnerability is found | Prioritize serious issues that have a remediation available. |
| Runtime image checks | `.env` or `pytest` is present, or missing configuration does not produce exit code 1 | Protect the production image and preserve expected configuration-error handling. |

Medium and Low findings, and High or Critical findings without an available fix, require review. They do not automatically pass as accepted risks: fix them or document the specific decision and evidence.

An accepted risk must identify the affected finding, why it is being tolerated, the mitigation, and a review date. A false positive must include evidence that the finding does not apply.

## Bandit (code)

Command: `uv run bandit main.py`

Result: No issues identified in `main.py` (105 lines).

The earlier recursive scan included `.venv` and test code. The production scan is therefore restricted to `main.py`.

The `B101: assert_used` finding was in `test_main.py`. The assertion is an intentional test assertion, not an application security check. The test file is excluded from this production-code scan.

## pip-audit (locked dependencies)

The dependencies were exported from `uv.lock` to a PEP 751 `pylock.toml` file and audited with `pip-audit --locked`.

Result: No known vulnerabilities found in the dependencies checked.

## Trivy (Dockerfile configuration)

- **DS-0002 (High): Fixed.** The Dockerfile creates `appuser` and switches to that non-root user.
- **DS-0026 (Low): Not applicable to the current use case.** The container runs a command and exits instead of operating as a long-running service. A Docker health check would not provide a meaningful health signal for this use case. Reconsider this decision if the container becomes a service.

## Trivy (image secrets)

Result: No secrets detected in the image by the secret scan performed.

## Trivy (image vulnerabilities)

The initial full scan reported 172 findings. After rebuilding with `--pull` and adding `apt-get upgrade`, the image still reports 44 High-severity vulnerabilities and 0 Critical vulnerabilities.

The findings are in Debian 13 (Trixie) system packages. Multiple packages can be affected by the same CVE, so the finding count is not the number of unique vulnerabilities.

### High-severity findings

| CVE | Affected package group | Current decision |
|---|---|---|
| CVE-2025-69720 | ncurses packages | Pending remediation; the Debian Trixie package remains flagged. |
| CVE-2026-16742 | systemd libraries | Pending applicability review; the advisory concerns systemd-homed, which this container does not run. Do not treat this alone as proof of a false positive. |
| CVE-2026-54369 | libacl1 | Pending remediation and applicability review. |
| CVE-2026-76642 | util-linux packages | Pending remediation; the Debian Trixie package remains flagged. |
| CVE-2026-78408 | util-linux packages | Pending remediation; the Debian Trixie package remains flagged. |
| CVE-2026-78409 | util-linux packages | Pending remediation; the Debian Trixie package remains flagged. |
| CVE-2026-78410 | util-linux packages | Pending remediation; the Debian Trixie package remains flagged. |
| CVE-2026-9538 | perl-base | Review the reported `fix_deferred` status and applicability. |

The package-level details are available in the Trivy report. The Debian tracker should be checked again before deciding that a finding is fixed or not applicable.

### Mitigations and follow-up

- The container runs as a non-root user.
- The container runs a command and exits; it is not a long-running network service.
- No findings are marked fixed or false positive solely because the application does not intentionally use the affected utility.
- Recheck the findings after Debian publishes relevant updates and rebuild the image.
- Review date: 2026-11-12.