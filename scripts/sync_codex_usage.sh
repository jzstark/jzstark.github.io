#!/usr/bin/env bash
# Run on the computer where Codex is signed in. Publish only the aggregate JSON.
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source_dir=$(dirname -- "$script_dir")
repository=${CODEX_ACTIVITY_REPOSITORY:-$(git -C "$source_dir" remote get-url origin)}
branch=${CODEX_ACTIVITY_BRANCH:-master}
state_dir=${CODEX_ACTIVITY_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/codex-activity}
codex_bin=${CODEX_BIN:-codex}

export GIT_TERMINAL_PROMPT=0
mkdir -p -- "$state_dir"
exec 9>"$state_dir/sync.lock"
flock -n 9 || exit 0
checkout=$(mktemp -d "$state_dir/run.XXXXXXXX")
trap 'rm -rf -- "$checkout"' EXIT

# A fresh checkout avoids staging, committing, or resetting the user's working tree.
git clone --quiet --depth 1 --single-branch --branch "$branch" -- "$repository" "$checkout"
if [[ ! -f "$checkout/activity.html" ]]; then
  echo 'Publish the activity page before enabling automatic updates.' >&2
  exit 1
fi

python3 "$script_dir/export_codex_usage.py" --codex "$codex_bin" \
  --output "$checkout/assets/data/codex-usage.json"
git -C "$checkout" add -- assets/data/codex-usage.json
if git -C "$checkout" diff --cached --quiet; then
  echo 'Usage data is already up to date.'
  exit 0
fi
git -C "$checkout" -c user.name='Codex Activity' \
  -c user.email='codex-activity@users.noreply.github.com' \
  commit --quiet -m 'Update Codex daily activity'
# Never force a push. A concurrent change is picked up by the next scheduled run.
git -C "$checkout" push origin "HEAD:refs/heads/$branch"
echo 'Published Codex daily activity.'
