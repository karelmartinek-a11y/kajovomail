# KajovoMail Android

Android Studio project implemented in Kotlin + Jetpack Compose. The UI speaks to `/api/v1` and `/events/ws`, keeps state in RAM, and stores the CSRF/session token inside EncryptedSharedPreferences.

## Getting started
1. Open `android` folder in Android Studio (requires Kotlin 1.9+ and Compose 1.6+).
2. Populate `local.properties` with `sdk.dir`.
3. Run `./gradlew assembleDebug` for a debug APK (or `connectedAndroidTest` to run Compose tests).

## Features
- Screens for login, accounts/folders, message list/detail, compose/reply, AI panel, offers, and settings.
- Virtual views, draft sending, AI orchestration simulations, and offer list UI.
- Encrypted session storage, network wiring via `ApiRepository`, and Compose navigation.
- Compose UI test in `androidTest` plus a unit test for the view model.

## Builds
- `./gradlew assembleDebug` produces `app/build/outputs/apk/debug/app-debug.apk`.
- `./gradlew bundleRelease` produces `app/build/outputs/bundle/release/app-release.aab`.
- Use `CAJOVOMAIL_API_BASE` gradle build config for pointing to the backend host.
