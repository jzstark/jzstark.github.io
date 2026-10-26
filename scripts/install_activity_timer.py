#!/usr/bin/env python3
"""Install a daily systemd user timer for this checkout's Codex activity updater."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess


def quoted(value):
    # systemd specifiers are expanded even inside quoted values.
    return json.dumps(str(value).replace("%", "%%"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print units without installing them")
    parser.add_argument("--repository", default="https://github.com/jzstark/jzstark.github.io.git")
    parser.add_argument("--branch", default="master")
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    codex = shutil.which("codex")
    if not codex:
        parser.error("codex must be on PATH; sign in with Codex before installing the timer")
    path = f"{Path(codex).parent}:{Path.home() / '.local/bin'}:/usr/local/bin:/usr/bin:/bin"
    service = f"""[Unit]
Description=Publish daily Codex activity to GitHub Pages
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash {quoted(script_dir / 'sync_codex_usage.sh')}
Environment={quoted('PATH=' + path)}
Environment={quoted('CODEX_BIN=' + codex)}
Environment={quoted('CODEX_ACTIVITY_REPOSITORY=' + args.repository)}
Environment={quoted('CODEX_ACTIVITY_BRANCH=' + args.branch)}
TimeoutStartSec=180
UMask=0077
"""
    timer = """[Unit]
Description=Sync Codex activity every morning

[Timer]
OnCalendar=*-*-* 09:00:00 Europe/Berlin
RandomizedDelaySec=15m
Persistent=true

[Install]
WantedBy=timers.target
"""
    units = {"codex-activity.service": service, "codex-activity.timer": timer}
    if args.dry_run:
        for name, content in units.items():
            print(f"# {name}\n{content}")
        return
    subprocess.run(["systemctl", "--user", "show-environment"], check=True, stdout=subprocess.DEVNULL)
    directory = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "systemd/user"
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in units.items():
        destination = directory / name
        destination.write_text(content, encoding="utf-8")
        destination.chmod(0o644)
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "--user", "enable", "--now", "codex-activity.timer"], check=True)
    print("Installed daily sync at 09:00–09:15 Europe/Berlin. Missed runs catch up when the user timer starts.")


if __name__ == "__main__":
    main()
