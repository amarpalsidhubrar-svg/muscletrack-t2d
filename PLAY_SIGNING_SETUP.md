# Google Play upload-key setup

MuscleTrack T2D uses Google Play App Signing. Keep the upload keystore private and never commit it to Git.

## 1. Generate the upload key locally

Run this on a trusted computer with Java installed:

```bash
keytool -genkeypair -v \
  -keystore muscletrack-upload-key.jks \
  -alias muscletrack-upload \
  -keyalg RSA \
  -keysize 4096 \
  -validity 10000
```

Choose and securely store the keystore password and key password. Keep `muscletrack-upload-key.jks` backed up in a secure location.

## 2. Convert the keystore to base64 for GitHub Actions

### macOS / Linux
```bash
base64 -w 0 muscletrack-upload-key.jks > muscletrack-upload-key.b64
```

If macOS does not support `-w`:
```bash
base64 < muscletrack-upload-key.jks | tr -d '\n' > muscletrack-upload-key.b64
```

### Windows PowerShell
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("muscletrack-upload-key.jks")) | Set-Content -NoNewline muscletrack-upload-key.b64
```

## 3. Add GitHub repository secrets

In the GitHub repository, go to **Settings → Secrets and variables → Actions → New repository secret** and add:

- `ANDROID_UPLOAD_KEYSTORE_BASE64` = contents of `muscletrack-upload-key.b64`
- `ANDROID_KEYSTORE_PASSWORD` = the keystore password
- `ANDROID_KEY_ALIAS` = `muscletrack-upload`
- `ANDROID_KEY_PASSWORD` = the key password

Do not paste the passwords or keystore into chat, issues, commits or pull requests.

## 4. Build the signed AAB

In GitHub open **Actions → Google Play signed AAB → Run workflow**.

If successful, download the `muscletrack-t2d-play-aab` artifact. The `.aab` inside is the file to upload to Google Play Console.

## 5. Play App Signing

When creating the first Play release, use Google Play App Signing and let Google generate/hold the app-signing key. Your upload key is used only to authenticate future app-bundle uploads.
