# craft-sonar

SonarCloud scans of the zuujiscom craft mirrors (the repos in `repos.txt`), reported to the SonarCloud
organization `zuujiscom` as projects `zuujiscom_<repo>`.

The mirrors stay identical to storytold's `main` ([craft-fork-sync](https://github.com/zuujiscom/craft-fork-sync)),
so storytold's own `sonarcloud.yml` is switched off in them (it reports to storytold's organization) and the
scans run here instead: every 2 hours, each mirror whose `main` moved since its last scan is checked out and
scanned. Results: [STATUS.md](STATUS.md) and SonarCloud.

Run now: Actions › SonarCloud › Run workflow (optionally name repos, or force a rescan).
