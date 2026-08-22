# MuscleTrack T2D — Version 0.1

A Flutter Android MVP for **monitoring** weight, activity, strength, body-composition entries and medication exposure in adults with type 2 diabetes.

## Intended use

This app is a monitoring and visualisation tool only. It does **not** diagnose disease, treat disease, recommend therapy, advise medication changes, or prescribe diet/exercise.

## Included in v0.1

- Local onboarding: name/nickname, adult age, sex, height, baseline weight
- Weight log with optional body-fat % and lean-mass entry
- Medication exposure timeline (GLP-1RA, dual GIP/GLP-1, SGLT2 inhibitor and other classes)
- Strength-session logging with multiple exercises, sets, reps and load
- Automatic training-volume calculation
- Estimated 1RM using the Epley equation for trend monitoring
- General activity/cardio logging with duration, optional MET and device calories
- MET-min calculation
- Estimated energy expenditure when MET is entered and device calories are unavailable
- User-defined weight, activity and strength goals
- Weight trend and recorded strength bests
- Local SQLite storage only
- Full local-data deletion control

## Not yet in v0.1

- Health Connect / smartwatch integration
- User accounts or cloud sync
- Clinician/research dashboard
- Data export / research upload
- Notifications
- Android production signing
- Google Play listing assets and final privacy policy

## Dependencies

- Flutter / Dart 3.x
- `sqflite` 2.4.3
- `path` 1.9.1

## Create Android platform files

This source bundle contains the application code and a bootstrap script. With Flutter installed:

```bash
chmod +x tool/bootstrap_android.sh
./tool/bootstrap_android.sh
flutter run
```

The script creates the standard Android runner project without overwriting `lib/` or `pubspec.yaml`.

## Build a test APK

```bash
flutter build apk --debug
```

## Build an app bundle

After configuring your production signing key and package identity:

```bash
flutter build appbundle --release
```

The resulting `.aab` is the format used for Google Play submission, but production signing and Play Console declarations remain publisher-owned steps.

## Working package / app identity

- Project: `muscletrack_t2d`
- Provisional Android application ID after bootstrap: `au.com.muscletrack.t2d`
- Working display name: **MuscleTrack T2D**

All of these can be renamed before Play Store submission.
