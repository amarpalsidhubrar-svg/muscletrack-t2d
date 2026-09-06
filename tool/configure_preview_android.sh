#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Give the preview APK a separate application ID so it can be installed
# alongside the Google Play closed-test build without touching its data.
while IFS= read -r -d '' file; do
  sed -i 's/au\.com\.muscletrack\.t2d/au.com.muscletrack.t2d.preview/g' "$file"
done < <(grep -rlZ 'au\.com\.muscletrack\.t2d' "$ROOT/android" || true)

MANIFEST="$ROOT/android/app/src/main/AndroidManifest.xml"
if [[ -f "$MANIFEST" ]]; then
  sed -i 's/android:label="muscletrack_t2d"/android:label="MuscleTrack T2D Preview"/' "$MANIFEST"
  sed -i 's/android:label="MuscleTrack T2D"/android:label="MuscleTrack T2D Preview"/' "$MANIFEST"
fi

echo "Preview Android app configured as au.com.muscletrack.t2d.preview"
