#!/usr/bin/env python3
"""Decides which mirrors to scan and records the results.

    scan.py plan [--force] [repo...]   prints `matrix=<json>` for $GITHUB_OUTPUT: every repo in repos.txt
                                       (or the ones named) whose main moved since its last scan
    scan.py record <results dir>       reads <results dir>/result-<repo>/result.json, rewrites
                                       scanned.json and STATUS.md

The mirrors are zuujiscom/<repo>, kept equal to storytold's main by craft-fork-sync, so nothing here
touches them: each scan checks out the mirror and sends it to SonarCloud organization zuujiscom
as project zuujiscom_<repo>.
"""
import datetime, glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OWNER = "zuujiscom"


def repos():
    return [l.strip() for l in open(os.path.join(ROOT, "repos.txt")) if l.strip() and not l.startswith("#")]


def scanned():
    return json.load(open(os.path.join(ROOT, "scanned.json")))


def head(repo):
    out = subprocess.run(["gh", "api", f"repos/{OWNER}/{repo}/commits/main", "-q", ".sha"],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def plan(args):
    force = "--force" in args
    names = [a for a in args if a != "--force"] or repos()
    done = scanned()
    todo = []
    for repo in names:
        sha = head(repo)
        if force or done.get(repo, {}).get("sha") != sha:
            todo.append({"repo": repo, "sha": sha})
    print(f"matrix={json.dumps(todo)}")
    print(f"scan: {', '.join(t['repo'] for t in todo) or 'nothing new'}", file=sys.stderr)


def record(results_dir):
    done = scanned()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ran = []
    for path in sorted(glob.glob(os.path.join(results_dir, "result-*", "result.json"))):
        r = json.load(open(path))
        ran.append(r)
        if r["ok"]:
            done[r["repo"]] = {"sha": r["sha"], "at": now}
    json.dump(done, open(os.path.join(ROOT, "scanned.json"), "w"), indent=2, sort_keys=True)
    open(os.path.join(ROOT, "scanned.json"), "a").write("\n")
    with open(os.path.join(ROOT, "STATUS.md"), "w") as f:
        f.write(f"# Status\n\nLast run {now}.\n\n")
        if ran:
            f.write("| Repo | Commit | Result |\n| --- | --- | --- |\n")
            for r in ran:
                f.write(f"| {r['repo']} | {r['sha'][:10]} | {'scanned' if r['ok'] else 'failed (see the run log)'} |\n")
        f.write("\n## Last good scan\n\n| Repo | Commit | When | SonarCloud |\n| --- | --- | --- | --- |\n")
        for repo in repos():
            e = done.get(repo)
            link = f"[zuujiscom_{repo}](https://sonarcloud.io/project/overview?id=zuujiscom_{repo})"
            f.write(f"| {repo} | {e['sha'][:10] if e else '-'} | {e['at'] if e else 'never'} | {link} |\n")
    print("\n".join(f"{r['repo']}: {'scanned' if r['ok'] else 'failed'}" for r in ran) or "nothing ran")


if __name__ == "__main__":
    if sys.argv[1:2] == ["plan"]:
        plan(sys.argv[2:])
    elif sys.argv[1:2] == ["record"] and len(sys.argv) == 3:
        record(sys.argv[2])
    else:
        sys.exit(__doc__)
