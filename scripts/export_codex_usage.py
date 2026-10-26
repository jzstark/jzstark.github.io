#!/usr/bin/env python3
"""Export only public, aggregate usage from the official Codex app-server."""

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time


ROOT = Path(__file__).resolve().parent.parent
SOURCE = {
    "id": "codex-account-usage",
    "name": "Codex account usage",
    "url": "https://learn.chatgpt.com/docs/app-server#7-token-usage-chatgpt",
}
SUMMARY_FIELDS = (
    "lifetimeTokens", "peakDailyTokens", "currentStreakDays", "longestStreakDays"
)
MAX_INTEGER = 2**53 - 1


class UsageError(Exception):
    pass


def read_account_usage(codex="codex", timeout=60):
    """Use the existing Codex login; never read or export authentication files."""
    messages = queue.Queue()
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen(
            [codex, "app-server", "--stdio", "-c", "analytics.enabled=false"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors,
            text=True, encoding="utf-8",
        )

        def receive():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except json.JSONDecodeError:
                    continue
            messages.put(None)

        reader = threading.Thread(target=receive, daemon=True)
        reader.start()
        deadline = time.monotonic() + timeout

        def send(message):
            process.stdin.write(json.dumps(message) + "\n")
            process.stdin.flush()

        def response(request_id):
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise UsageError("Codex usage request timed out; the saved data is unchanged.")
                try:
                    message = messages.get(timeout=remaining)
                except queue.Empty as exc:
                    raise UsageError("Codex usage request timed out; the saved data is unchanged.") from exc
                if message is None:
                    raise UsageError("Codex app-server exited. Check its login and filesystem access.")
                if message.get("id") != request_id:
                    continue
                if "error" in message:
                    code = message["error"].get("code", "unknown")
                    raise UsageError(
                        f"Codex rejected the usage request (code {code}). "
                        "Check your Codex login and account access; the saved data is unchanged."
                    )
                return message.get("result")

        try:
            send({
                "id": 1, "method": "initialize",
                "params": {
                    "clientInfo": {"name": "personal_codex_activity", "version": "1.0.0"},
                    "capabilities": {"experimentalApi": True},
                },
            })
            response(1)
            send({"method": "initialized", "params": {}})
            send({"id": 2, "method": "account/usage/read"})
            return response(2)
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            reader.join(timeout=1)
            process.stdin.close()
            process.stdout.close()


def count(value):
    if type(value) is not int or not 0 <= value <= MAX_INTEGER:
        raise UsageError("The usage response contains an invalid token count.")
    return value


def day_key(value):
    if not isinstance(value, str):
        raise UsageError("The usage response contains an invalid date.")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise UsageError("The usage response contains an invalid date.") from exc
    if parsed.isoformat() != value:
        raise UsageError("The usage response contains a non-canonical date.")
    return value


def public_snapshot(result, previous=None, now=None):
    """Allowlist fields; retain older observed days without inventing missing zeros."""
    if not isinstance(result, dict):
        raise UsageError("Codex returned an invalid usage response.")
    buckets = result.get("dailyUsageBuckets")
    if not isinstance(buckets, list) or not buckets:
        raise UsageError("Codex returned no daily usage history; the saved data is unchanged.")
    days = {}
    if previous:
        if previous.get("schema_version") != 1 or previous.get("source", {}).get("id") != SOURCE["id"]:
            raise UsageError("Existing data has a different source or schema; refusing to merge it.")
        for item in previous.get("days", []):
            days[day_key(item["date"])] = count(item["tokens"])
    received = set()
    for bucket in buckets:
        if not isinstance(bucket, dict):
            raise UsageError("Codex returned an invalid daily bucket.")
        day = day_key(bucket.get("startDate"))
        if day in received:
            raise UsageError("Codex returned duplicate daily buckets; refusing to double-count them.")
        received.add(day)
        # A new snapshot replaces an existing day's count, including downward corrections.
        days[day] = count(bucket.get("tokens"))
    raw_summary = result.get("summary") or {}
    if not isinstance(raw_summary, dict):
        raise UsageError("Codex returned an invalid usage summary.")
    summary = {
        key: count(raw_summary[key]) if raw_summary.get(key) is not None else None
        for key in SUMMARY_FIELDS
    }
    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return {
        "schema_version": 1,
        "source": SOURCE,
        "updated_at": timestamp.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "summary": summary,
        "days": [{"date": day, "tokens": days[day]} for day in sorted(days)],
    }


def save_snapshot(path, snapshot):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(snapshot, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex", help="Codex executable (uses its existing login)")
    parser.add_argument("--output", type=Path, default=ROOT / "assets/data/codex-usage.json")
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    try:
        previous = json.loads(args.output.read_text()) if args.output.exists() else None
        snapshot = public_snapshot(read_account_usage(args.codex, args.timeout), previous)
        save_snapshot(args.output, snapshot)
        print(f"Saved {len(snapshot['days'])} reported days to {args.output}.")
    except (UsageError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Usage export failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
