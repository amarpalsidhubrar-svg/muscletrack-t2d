# MuscleTrack T2D — Google Play release checklist

## Technical release readiness
- [x] Flutter Android app builds and runs on a physical Android phone
- [x] Monitoring-only positioning: no diagnosis, treatment or medication-change advice
- [x] Package/application ID: `au.com.muscletrack.t2d`
- [x] Version: `0.1.0+1`
- [x] Target Android 16 / API 36
- [x] Local SQLite storage
- [x] No analytics, advertising or developer-operated cloud backend in v0.1
- [x] In-app privacy/data-practices text
- [x] Public privacy-policy HTML draft in `docs/privacy-policy.html`
- [x] Signed AAB GitHub workflow prepared

## Publisher-owned steps
1. Create or confirm a Google Play Developer account and complete identity verification.
2. In Play Console, create a new app named **MuscleTrack T2D** with package ID `au.com.muscletrack.t2d`.
3. Generate and securely retain an Android upload keystore. Do not commit the `.jks` file or passwords to Git.
4. Add four GitHub Actions repository secrets:
   - `ANDROID_UPLOAD_KEYSTORE_BASE64`
   - `ANDROID_KEYSTORE_PASSWORD`
   - `ANDROID_KEY_ALIAS`
   - `ANDROID_KEY_PASSWORD`
5. Run `.github/workflows/play-release-build.yml` manually to produce the signed `app-release.aab` artifact.
6. Enable Google Play App Signing when creating the first Play release.
7. Make the privacy policy publicly accessible (recommended: enable GitHub Pages from `/docs`) and enter the resulting URL in Play Console.
8. Complete the Data safety form.
9. Complete the Health apps declaration.
10. Complete content rating, target audience, ads declaration, app access, store listing and developer contact fields.
11. Upload store assets and screenshots.
12. Upload the signed `.aab` to an internal or closed testing track.

## Suggested Health apps declaration for v0.1
Declare all functionality actually present:
- **Activity and Fitness** — records exercise, workouts, body weight/body composition.
- **Nutrition and Weight Management** — supports weight-management goals and weight tracking (no dietary prescription).
- **Diseases and Conditions Management** — the app is specifically intended for adults living with type 2 diabetes and provides monitoring/self-tracking.

Do **not** select for v0.1:
- Medical Device Apps
- Clinical Decision Support
- Emergency and First Aid
- Research studies / clinical trials

Medication names/doses are recorded as a timeline, but v0.1 does not provide medication reminders, adherence management or treatment recommendations.

## Suggested Data safety position for v0.1
Based on the current code and dependencies, user-entered data stays on the device and is not transmitted off-device by the app. Google defines 'collect' as transmitting data off a user's device and states that purely on-device access/processing does not need to be disclosed as collected.

Subject to final Play Console review of the exact production build:
- Data collected off-device by developer: **No**
- Data shared with third parties: **No**
- Ads: **No**

If Health Connect, analytics, crash reporting, cloud sync, research upload or external SDKs are added later, these declarations must be revisited before publishing the update.

## Privacy policy URL
Recommended after enabling GitHub Pages:
`https://amarpalsidhubrar-svg.github.io/muscletrack-t2d/privacy-policy.html`

Do not submit the URL until it is confirmed publicly accessible in a normal browser.

## Store assets required
- 512 x 512 PNG app icon
- 1024 x 500 feature graphic
- Minimum 2 phone screenshots
- Store listing text (draft already in `PLAY_STORE_LISTING.md`)

## Testing requirement that may apply
For a **personal Play Developer account created after 13 November 2023**, Google requires a closed test with at least **12 testers continuously opted in for 14 days** before production access can be requested. Older accounts and organization accounts may follow different eligibility rules shown in that account's Play Console.
