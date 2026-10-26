import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("exporter", ROOT / "scripts/export_codex_usage.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
NOW = datetime(2026, 10, 26, tzinfo=timezone.utc)


def response(buckets):
    return {"dailyUsageBuckets": buckets, "summary": {"lifetimeTokens": 1234}}


def fake_codex(path, result=None, error=False, hang=False):
    code = f"""#!/usr/bin/env python3
import json, sys, time
for line in sys.stdin:
    message = json.loads(line)
    if message['method'] == 'initialize':
        print(json.dumps({{'id': message['id'], 'result': {{}}}}), flush=True)
    elif message['method'] == 'account/usage/read':
        if {hang!r}: time.sleep(10)
        if {error!r}:
            print(json.dumps({{'id': message['id'], 'error': {{'code': -32000, 'message': 'Not signed in'}}}}), flush=True)
        else:
            print(json.dumps({{'id': message['id'], 'result': {result!r}}}), flush=True)
"""
    path.write_text(code)
    path.chmod(0o755)
    return str(path)


class UsageTests(unittest.TestCase):
    def test_allowlist_drops_private_fields_and_preserves_zero(self):
        raw = response([{"startDate": "2026-10-25", "tokens": 0, "prompt": "private"}])
        raw["threadUsage"] = {"threadId": "private-thread", "groups": []}
        raw["summary"]["accountId"] = "private-account"
        output = exporter.public_snapshot(raw, now=NOW)
        self.assertNotIn("private", json.dumps(output))
        self.assertEqual(output["days"], [{"date": "2026-10-25", "tokens": 0}])
        self.assertIsNone(output["summary"]["currentStreakDays"])

    def test_merge_replaces_counts_and_does_not_fill_missing_days(self):
        first = exporter.public_snapshot(response([
            {"startDate": "2026-10-22", "tokens": 20},
            {"startDate": "2026-10-24", "tokens": 30},
        ]), now=NOW)
        raw = response([{"startDate": "2026-10-24", "tokens": 15}])
        second = exporter.public_snapshot(raw, first, NOW)
        self.assertEqual(second["days"], [
            {"date": "2026-10-22", "tokens": 20},
            {"date": "2026-10-24", "tokens": 15},
        ])
        self.assertEqual(exporter.public_snapshot(raw, second, NOW), second)

    def test_rejects_empty_duplicate_and_invalid_history(self):
        for buckets in [None, [], [{"startDate": "2026-02-30", "tokens": 1}],
                        [{"startDate": "2026-10-25", "tokens": True}],
                        [{"startDate": "2026-10-25", "tokens": -1}],
                        [{"startDate": "2026-10-25", "tokens": 2**53}],
                        [{"startDate": "2026-10-25", "tokens": 1}] * 2]:
            with self.subTest(buckets=buckets), self.assertRaises(exporter.UsageError):
                exporter.public_snapshot(response(buckets), now=NOW)

    def test_protocol_handshake_and_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "codex"
            raw = response([{"startDate": "2026-10-25", "tokens": 42}])
            self.assertEqual(exporter.read_account_usage(fake_codex(binary, raw), 2), raw)
            with self.assertRaises(exporter.UsageError):
                exporter.read_account_usage(fake_codex(binary, hang=True), 0.1)

    def test_failed_refresh_does_not_replace_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "usage.json"
            previous = exporter.public_snapshot(response([{"startDate": "2026-10-25", "tokens": 42}]), now=NOW)
            exporter.save_snapshot(output, previous)
            original = output.read_bytes()
            binary = fake_codex(Path(directory) / "codex", error=True)
            result = subprocess.run(["python3", str(ROOT / "scripts/export_codex_usage.py"), "--codex", binary,
                                     "--output", str(output)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(output.read_bytes(), original)

    def test_sync_publishes_only_data_to_an_isolated_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            remote, seed = base / "remote.git", base / "seed"

            def git(*args, cwd=None):
                return subprocess.check_output(["git", *map(str, args)], cwd=cwd, stderr=subprocess.DEVNULL, text=True).strip()

            git("init", "--bare", remote)
            git("init", "-b", "main", seed)
            (seed / "activity.html").write_text("activity page")
            git("add", ".", cwd=seed)
            git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "Initial page", cwd=seed)
            git("remote", "add", "origin", remote, cwd=seed)
            git("push", "origin", "main", cwd=seed)
            (seed / "activity.html").write_text("uncommitted user edits")
            binary = fake_codex(base / "codex", response([{"startDate": "2026-10-25", "tokens": 42}]))
            environment = {**os.environ, "CODEX_ACTIVITY_REPOSITORY": str(remote), "CODEX_ACTIVITY_BRANCH": "main",
                           "CODEX_ACTIVITY_STATE_DIR": str(base / "state"), "CODEX_BIN": binary}
            subprocess.run(["bash", str(ROOT / "scripts/sync_codex_usage.sh")], env=environment,
                           check=True, capture_output=True)
            changed = git("--git-dir", remote, "diff-tree", "--no-commit-id", "--name-only", "-r", "main")
            self.assertEqual(changed, "assets/data/codex-usage.json")
            self.assertEqual((seed / "activity.html").read_text(), "uncommitted user edits")
            self.assertEqual(list((base / "state").glob("run.*")), [])


if __name__ == "__main__":
    unittest.main()
