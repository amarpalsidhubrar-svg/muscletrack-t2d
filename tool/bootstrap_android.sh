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

# Keep the Android application ID and launcher Activity package aligned.
while IFS= read -r -d '' file; do
  sed -i 's/au\.com\.muscletrack\.muscletrack_t2d/au.com.muscletrack.t2d/g' "$file"
done < <(grep -rlZ 'au\.com\.muscletrack\.muscletrack_t2d' "$ROOT/android" || true)

# Target Android 16 / API 36 for Google Play submissions from 31 Aug 2026.
APP_GRADLE="$ROOT/android/app/build.gradle.kts"
if [[ -f "$APP_GRADLE" ]]; then
  sed -i 's/compileSdk = flutter\.compileSdkVersion/compileSdk = 36/' "$APP_GRADLE"
  sed -i 's/targetSdk = flutter\.targetSdkVersion/targetSdk = 36/' "$APP_GRADLE"
fi

cd "$ROOT"
flutter pub get

echo "Android runner created with application ID au.com.muscletrack.t2d and targetSdk 36"
