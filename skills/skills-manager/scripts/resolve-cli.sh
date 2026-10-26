#!/usr/bin/env bash
# Resolves the skills-manager-cli binary path across desktop app, version stamp, and PATH

D="$HOME/.skills-manager/bin"
B="$D/skills-manager-cli"
[ -e "$B" ] || B="$B.exe"

if [ -s "$D/.version" ] && [ -x "$B" ]; then
  echo "$B"
elif [ -s "$D/.version" ] || [ -e "$B" ]; then
  echo "BRIDGE_BROKEN"
else
  P="$(command -v skills-manager-cli 2>/dev/null || true)"
  if [ -x "$P" ]; then
    echo "$P"
  else
    echo "NOT_FOUND"
  fi
fi
