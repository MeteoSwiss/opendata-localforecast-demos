# Dependency update 2026-11-11

Security only: fixable critical and high CVEs, applied with a targeted lock refresh
(`poetry update --lock pillow matplotlib certifi anyio aiohttp tornado jupyter-client urllib3`).
`pyproject.toml` is unchanged. All other upgrades come in a later PR.

| Package | Old → new | Why (CVE / deprecated / outdated) | Breaking changes and how they were handled |
| --- | --- | --- | --- |
| pillow | 12.2.0 → 13.0.0 (Python ≥ 3.11); 12.2.0 → 12.3.0 (Python 3.10) | 54 CVEs/GHSAs (5 critical, 33 high, 16 medium), e.g. CVE-2026-112393, CVE-2026-112398, CVE-2026-112403, CVE-2026-112900, CVE-2026-96639, GHSA-78g4-xqwv-q3g8 | Major version. Only matplotlib uses it, never the project's code. Both notebooks run; `solar_production.png` is identical and `meteogram.png` differs by 4 pixels (glyph rendering). |
| matplotlib | 3.11.0 → 3.11.2 | updated together with pillow (it depends on it) | patch release, none |
| certifi | 2026.6.17 → 2026.10.23 | GHSA-6q48-6c7w-9gw2 (critical: compromised emSign root CAs) | none |
| anyio | 4.14.1 → 4.16.0 | CVE-2026-63374 (critical), CVE-2026-63349 (high), CVE-2026-64847 | minor, via httpx; notebooks download data as before |
| aiohttp | 3.14.1 → 3.14.5 | 11 CVEs (4 high), e.g. CVE-2026-69244, CVE-2026-111064, CVE-2026-111066, CVE-2026-123817 | patch; only installed on Python 3.12 (papermill) |
| yarl | 1.24.2 → 1.25.1 | came along with aiohttp (Python 3.12 only) | minor, no CVE |
| tornado | 6.5.7 → 6.6.1 (Python ≥ 3.11); 6.5.7 → 6.5.10 (Python 3.10) | 9 issues (3 high), e.g. CVE-2026-82397, GHSA-c2m8-h5v5-343r, GHSA-chx6-46f5-w4vp | minor; Jupyter kernel runs the notebooks fine |
| jupyter-client | 8.9.1 → 8.10.0 | updated together with tornado (it depends on it) | minor, none |
| urllib3 | 2.7.0 → 2.8.0 | CVE-2026-97687, CVE-2026-97689 (high), CVE-2026-97688 | minor, none |
| typing-extensions | 4.15.0 → 4.16.0 | came along with the targeted update | minor, none |

## Not upgraded
| Package | Latest | Why not | Waiting for |
| --- | --- | --- | --- |
| pillow on Python 3.10 | 13.0.0 | Python version: pillow 13 needs Python ≥ 3.11. 41 CVEs stay open on 3.10 only (5 critical, 23 high, 13 medium) | `fix-platform`: drop Python 3.10 (end of life) from `requires-python` |
| tornado on Python 3.10 | 6.6.1 | Python version: tornado 6.6 needs Python ≥ 3.11. 3 CVEs stay open on 3.10 only (CVE-2026-115927, CVE-2026-116577, CVE-2026-116578) | `fix-platform`: drop Python 3.10 |
| pylint | 4.1.3 | user decision: medium CVE-2026-114608 needs a constraint change (`^3.3.5` → 4.x), second run | second `fix-dependencies` run |
| pytest | 9.2.0 | user decision: medium CVE-2025-71176 needs a constraint change (`^8.3.5` → 9.x), second run | second `fix-dependencies` run |
| soupsieve | 4.1 | user decision: medium only (CVE-2026-85999, CVE-2026-86000), second run | second `fix-dependencies` run |
| multidict | 7.2.1 | user decision: medium only (CVE-2026-104874), second run | second `fix-dependencies` run |

No CVE without a fixed version was found, and no issue has to wait for another project's fix.

## Checks
| Check | Result |
| --- | --- |
| `poetry check --lock` and `poetry install --with dev` (Python 3.11.15) | ok |
| Lock diff (`tomllib`) | only the packages above changed |
| Notebooks via papermill, old lock and new lock | `Meteogram.ipynb` and `SolarProduction.ipynb` run on both, same data (model run 2026-11-11 16:00 CET) |
| Output images | `solar_production.png` identical; `meteogram.png` same size, 4 pixels differ in a 10×8 px area |
| mypy | 22 errors before and after (unchanged, code-quality findings) |
| pylint | 9.61/10 before and after |
| `trivy fs --scanners vuln --include-dev-deps --ignore-unfixed` | all planned CVEs gone on Python ≥ 3.11; 49 remain: 44 pillow 12.3.0 / tornado 6.5.10 (Python 3.10 only) and 5 medium deferred above; no new ones |
| Test suite | skipped: the repository has no tests (the notebook runs stand in for them) |
| Image build | not applicable: no Dockerfile |
