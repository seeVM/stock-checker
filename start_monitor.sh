#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# load .env safely (export all variables from file)
if [ -f .env ]; then
  set -o allexport
  # shellcheck disable=SC1091
  . ./.env
  set +o allexport
fi

# activate venv
source venv/bin/activate

# ensure logs folder
mkdir -p logs

# run monitor & save output
exec python3 -u -m scripts.monitor 2>&1 | tee -a logs/monitor.log
