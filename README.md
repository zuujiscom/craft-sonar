# craft-sonar

SonarCloud scans of zuujiscom repos, reported to the SonarCloud organization `zuujiscom` as projects
`zuujiscom_<repo>`. The repos scanned are the projects that exist in that organization: import a repo in
SonarCloud (CI-based analysis, not Automatic Analysis) and the next run picks it up. `repos.txt` is only a
fallback for when SonarCloud can't be reached. Projects with SonarCloud's Automatic Analysis on are skipped: SonarCloud
analyses those itself (it turns it on for languages it supports, e.g. Python and JavaScript, but not Rust).

The mirrors stay identical to storytold's `main` ([craft-fork-sync](https://github.com/zuujiscom/craft-fork-sync)),
so storytold's own `sonarcloud.yml` is switched off in them (it reports to storytold's organization) and the
scans run here instead: every 2 hours, each repo whose default branch moved since its last scan is checked out and
scanned. Results: [STATUS.md](STATUS.md) and SonarCloud.

Run now: Actions › SonarCloud › Run workflow (optionally name repos, or force a rescan).
