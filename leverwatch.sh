#!/usr/bin/env bash
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && { pwd -W 2>/dev/null || pwd; })"
SP="$(python "$KIT/kitpaths.py" state)"
ONCE=0
[ "$1" = "--once" ] && { ONCE=1; shift; }
INTERVAL="${1:-300}"
SEEN="${LEVERWATCH_SEEN:-$SP/wlog/leverwatch_seen.txt}"
# A bounded observation is useful for tests and one-off checks; zero watches indefinitely.
MAX_CYCLES="${LEVERWATCH_MAX_CYCLES:-0}"
CYCLES=0
touch "$SEEN"

while :; do
  fired=0
  while read -r addr text; do
    [ -n "$addr" ] || continue
    grep -qxF "$addr" "$SEEN" && continue
    echo "$addr" >> "$SEEN"
    echo "LEVER NEEDS PROMOTING $addr: $text"
    fired=1
  done < <(python "$KIT/levercheck.py" --keys 2>/dev/null)
  [ "$ONCE" = 1 ] && [ "$fired" = 1 ] && exit 0
  CYCLES=$((CYCLES + 1))
  [ "$MAX_CYCLES" -gt 0 ] && [ "$CYCLES" -ge "$MAX_CYCLES" ] && exit 0
  sleep "$INTERVAL"
done
