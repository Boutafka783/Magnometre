# Gradiometer

Android / Kotlin / Jetpack Compose app for ESP32 Bluetooth Classic (SPP) magnetic-gradient measurements, 2D/3D scan maps and community circuits.

## Requirements
- Android Studio with Android SDK 36
- JDK 17; Gradle 8.13; Android Gradle Plugin 8.13.2
- A Firebase project dedicated to Gradiometer (never reuse Zevorix Firebase config)
- Google Play Console one-time INAPP product `unlock_connection`
- Firebase CLI: `npm install -g firebase-tools`

## Firebase setup
1. Create a separate Firebase project and Android app package `com.example.gradiometer`.
2. Enable Anonymous Authentication, Firestore and Storage.
3. Download the Gradiometer project's `google-services.json` into `app/`. Do not copy Zevorix credentials.
4. In Firebase Console, create a Web App in the same Gradiometer project and copy its public web configuration into `account-deletion.html` and `public/account-deletion.html` (the web config is public; never put service-account keys in the page).
5. Enable Email/Password Authentication if you want direct web deletion for accounts linked to email/password. Anonymous-only accounts must use the in-app delete button or contact the support address on the deletion page.
6. Set the custom admin claim `admin: true` only for trusted moderator accounts using a protected Admin SDK process.

## Deploy Cloud Functions and security rules
Run these commands from the project root. Select the Gradiometer Firebase project explicitly; never select Zevorix:

```bash
firebase login
firebase projects:list
firebase use --add                 # choose the Gradiometer project and name the alias gradiometer
firebase use gradiometer
cd functions
npm install
cd ..
firebase deploy --only functions,firestore:rules,storage
```

The callable Functions are `deleteMyAccount`, `reportCircuit`, and `reviewCircuitReport`. The server-side report function repeats the same banned-phrase filter as the Android `ContentFilter` before accepting a report, prevents duplicate reports, counts unique reports, and hides a post at three reports. Admin review requires the Firebase Auth custom claim `admin: true`.

## Publish account deletion page (required for the Play Console web deletion URL)
1. Replace `REPLACE_WITH_SUPPORT_EMAIL` in `account-deletion.html` and `public/account-deletion.html` with a monitored support address.
2. Replace the Firebase Web App placeholders in `public/account-deletion.html` with the Web App configuration from the **Gradiometer** Firebase project.
3. Publish the site with Firebase Hosting:

```bash
firebase deploy --only hosting
```

4. The deletion page URL is `https://<YOUR_GRADIOMETER_PROJECT_ID>.web.app/account-deletion.html` (or your configured custom domain). Open it in a private browser and test the complete deletion flow with a test account before publishing this URL in Google Play Console under the account deletion URL field.
5. Also publish `privacy-policy.html` and enter its HTTPS URL in Play Console. Keep the support email active. Web self-service currently requires an email/password-linked account; anonymous accounts can delete from inside the Android app or request assistance using the page's support email.

The in-app **Delete my account** button calls `AccountDeletion.deleteCurrentAccount()`, which invokes the authenticated `deleteMyAccount` callable. The callable removes the user's Firestore profile, authored circuit posts, the user's `circuit_images/<uid>/` Storage files, and Firebase Authentication account.

## Google Play Billing
Create a one-time, non-consumable in-app product with exact ID `unlock_connection`. Add tester accounts and install from an internal testing track. The app queries owned purchases at startup and acknowledges completed purchases; pending purchases do not unlock. Do not create this product as a subscription or consumable.

## Release signing
Set `KEYSTORE_FILE`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, and `KEY_PASSWORD` in the build environment. Release builds intentionally do not fall back to debug signing. GitHub Actions additionally requires secrets `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`, and `GOOGLE_SERVICES_JSON` (base64-encoded JSON).

## Privacy / Data safety
See `privacy-policy.html` and `DATA_SAFETY_CHECKLIST.md`. These are templates: verify actual SDK data collection, replace all placeholders, host the policy, and make the Play Console declaration match production behavior.

## Store assets
Run `python scripts/generate_store_assets.py` after installing Pillow. The icon and feature graphic are temporary placeholders, not final branding. Add real screenshots following Play Console's current dimensions and device requirements.

## Build
```bash
gradle testDebugUnitTest
gradle bundleRelease
```
A release bundle requires all four signing environment variables and the Gradiometer `google-services.json`.
