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

The initial full scan reported:

| Severity | Findings |
|---|---:|
| High | 44 |
| Medium | 63 |
| Low | 62 |
| Unknown | 3 |
| **Total** | **172** |

These counts are a baseline, not individual risk decisions. Rebuild with the refreshed base image and scan again.

**Individual triage is still required.** For every remaining finding, record its vulnerability ID, package and installed version, severity, decision, reason and evidence. Fix the finding where practical; otherwise record a verified false positive or an accepted risk with a review date. Do not mark all findings as accepted risks based solely on the severity counts.
