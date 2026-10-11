#!/usr/bin/env python3
"""Android setup for the v0.3.9 daily reminder (flutter_local_notifications).

Run after tool/bootstrap_android.sh, which regenerates android/ each build.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT/'android/app'


def patch(path, old, new):
    text = path.read_text()
    if new in text:
        return
    if text.count(old) != 1:
        raise SystemExit(f'{path}: expected one match for {old!r}')
    path.write_text(text.replace(old, new))


# Reschedule after reboot/app update and show scheduled notifications.
manifest = APP/'src/main/AndroidManifest.xml'
patch(manifest, '    <application',
      '    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>\n'
      '    <application')
patch(manifest, '    </application>', '''        <receiver
            android:exported="false"
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver" />
        <receiver
            android:exported="false"
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED"/>
                <action android:name="android.intent.action.QUICKBOOT_POWERON" />
                <action android:name="com.htc.intent.action.QUICKBOOT_POWERON"/>
            </intent-filter>
        </receiver>
    </application>''')

# The plugin needs core library desugaring for scheduled notifications.
gradle = APP/'build.gradle.kts'
patch(gradle, '    compileOptions {\n',
      '    compileOptions {\n        isCoreLibraryDesugaringEnabled = true\n')
text = gradle.read_text()
if 'coreLibraryDesugaring(' not in text:
    gradle.write_text(text.rstrip() + '''

dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
}
''')

# Monochrome status-bar icon (dumbbell), kept from resource shrinking.
drawable = APP/'src/main/res/drawable'
drawable.mkdir(parents=True, exist_ok=True)
(drawable/'ic_stat_reminder.xml').write_text('''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFFFF"
        android:pathData="M20.57,14.86L22,13.43 20.57,12 17,15.57 8.43,7 12,3.43 10.57,2 9.14,3.43 7.71,2 5.57,4.14 4.14,2.71 2.71,4.14l1.43,1.43L2,7.71l1.43,1.43L2,10.57 3.43,12 7,8.43 15.57,17 12,20.57 13.43,22l1.43,-1.43L16.29,22l2.14,-2.14 1.43,1.43 1.43,-1.43 -1.43,-1.43L22,16.29z" />
</vector>
''')
raw = APP/'src/main/res/raw'
raw.mkdir(parents=True, exist_ok=True)
(raw/'keep.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@drawable/ic_stat_reminder" />
''')

print('Configured Android for daily reminder notifications')
