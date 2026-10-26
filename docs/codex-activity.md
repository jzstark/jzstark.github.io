# Codex Activity

The `/activity/` page is part of the existing Jekyll / Minima site. It reads
`assets/data/codex-usage.json`; no backend or visitor authentication is needed.

## Data source and interpretation

The exporter calls the documented Codex app-server `account/usage/read` method,
using the existing local Codex login:
https://learn.chatgpt.com/docs/app-server#7-token-usage-chatgpt

Only date/token pairs, four aggregate summary fields, the source, and a sync
timestamp are exported. Raw conversations, prompts, paths, account identifiers,
thread usage, and credentials are not copied into the website. No OpenAI API key
is required. API-key-only authentication cannot use this account endpoint.

Daily buckets and some summary fields can be unavailable. A missing/empty daily
response or a failed request exits nonzero and leaves the saved file untouched.
New buckets replace old counts for the same day rather than being added to them.
Older reported days are retained when they leave the upstream response window.
This means an old day can remain unchanged when upstream no longer supplies it;
the sync timestamp is not a claim that every historical day was freshly fetched.

The calendar uses dates exactly as supplied by Codex, with UTC determining the
current calendar date. The source does not document a bucket timezone here.
Missing dates are not assumed to be zeros. The 30-day cards exclude today, report
coverage, and divide the average by reported days, including explicit zero days.
Use this as Codex token activity, not as total ChatGPT activity, billing, hours,
or a productivity measurement. Local transcript estimates are not mixed into it.

## Collect once

With Python 3.9+ and a recent Codex version supporting `account/usage/read`:

```sh
python3 scripts/export_codex_usage.py
```

The script only starts app-server, performs its handshake, and reads account
usage. It does not start a model turn. It times out after 60 seconds. An alternate
Codex executable can be selected with `--codex /absolute/path/to/codex`.

## Publish and schedule

Publish the page and initial JSON to the existing GitHub Pages source branch
(`master`, repository root). With Codex and GitHub signed in on this computer:

```sh
bash scripts/sync_codex_usage.sh
python3 scripts/install_activity_timer.py
```

The sync script clones the latest `master` into a temporary directory, collects
usage, commits only `assets/data/codex-usage.json`, and pushes without force.
It never stages or changes the source checkout. A lock prevents overlapping runs;
temporary checkouts are removed on exit. Failed collection/push leaves the
published page available. A future run starts from the latest remote branch.

The systemd user timer runs at 09:00–09:15 Europe/Berlin each day, including DST.
`Persistent=true` catches up missed runs when the user timer next starts. The
computer needs network access and an active user service manager. This installer
does not enable system-wide services or lingering. A computer that is off cannot
publish until it is running again. The page marks data older than 48 hours.

Preview the generated units without installing: `python3 scripts/install_activity_timer.py --dry-run`.
The units are saved under `~/.config/systemd/user/` (or `$XDG_CONFIG_HOME`).
They reference this checkout and the current Codex executable. Re-run the installer
after moving the checkout or replacing the executable path, e.g. after an NVM upgrade.
Keep Codex and GitHub logged in; credentials stay in their existing local stores.

```sh
systemctl --user list-timers codex-activity.timer
systemctl --user start codex-activity.service
journalctl --user -u codex-activity.service -n 30
systemctl --user disable --now codex-activity.timer
```

Override `CODEX_ACTIVITY_REPOSITORY`, `CODEX_ACTIVITY_BRANCH`, `CODEX_BIN`, or
`CODEX_ACTIVITY_STATE_DIR` for a different destination or local testing. The
installer also accepts `--repository` and `--branch`.

## Verification

```sh
python3 -m unittest discover -s tests
node --test tests/activity.test.mjs
bash -n scripts/sync_codex_usage.sh
bundle exec jekyll build --destination /tmp/codex-activity-site
```

The Python tests include a fake Codex protocol server and an isolated local Git
remote to check timeout/error handling, public field filtering, snapshot merging,
and publishing only the data file. They make no real account requests or pushes.
