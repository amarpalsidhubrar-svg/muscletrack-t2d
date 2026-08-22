from pathlib import Path

path = Path('android/app/build.gradle.kts')
text = path.read_text()

prefix = '''import java.io.FileInputStream\nimport java.util.Properties\n\nval keystoreProperties = Properties()\nval keystorePropertiesFile = rootProject.file("key.properties")\nif (!keystorePropertiesFile.exists()) {\n    error("Missing android/key.properties for Play release signing")\n}\nkeystoreProperties.load(FileInputStream(keystorePropertiesFile))\n\n'''

if 'val keystoreProperties = Properties()' not in text:
    text = prefix + text

signing_block = '''\n    signingConfigs {\n        create("release") {\n            keyAlias = keystoreProperties["keyAlias"] as String\n            keyPassword = keystoreProperties["keyPassword"] as String\n            storeFile = file(keystoreProperties["storeFile"] as String)\n            storePassword = keystoreProperties["storePassword"] as String\n        }\n    }\n'''

if 'create("release")' not in text:
    marker = '    defaultConfig {'
    if marker not in text:
        raise SystemExit('Could not find defaultConfig block in Android Gradle file')
    text = text.replace(marker, signing_block + '\n' + marker, 1)

text = text.replace(
    'signingConfig = signingConfigs.getByName("debug")',
    'signingConfig = signingConfigs.getByName("release")'
)

# Enforce Play target level regardless of Flutter template defaults.
text = text.replace('compileSdk = flutter.compileSdkVersion', 'compileSdk = 36')
text = text.replace('targetSdk = flutter.targetSdkVersion', 'targetSdk = 36')

path.write_text(text)
print('Configured Android release signing and API 36 target.')
