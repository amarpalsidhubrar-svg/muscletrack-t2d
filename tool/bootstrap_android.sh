#!/usr/bin/env bash
set -euo pipefail

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is not installed or not on PATH." >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

flutter create \
  --platforms=android \
  --org au.com.muscletrack \
  --project-name muscletrack_t2d \
  "$TMP/muscletrack_t2d"

rm -rf "$ROOT/android"
cp -R "$TMP/muscletrack_t2d/android" "$ROOT/android"
cp "$TMP/muscletrack_t2d/.metadata" "$ROOT/.metadata"

find "$ROOT/android" -type f \( -name '*.gradle' -o -name '*.kts' \) -print0 | \
  xargs -0 sed -i 's/au\.com\.muscletrack\.muscletrack_t2d/au.com.muscletrack.t2d/g'

cd "$ROOT"
flutter pub get

echo "Android runner created. Next: flutter run"
