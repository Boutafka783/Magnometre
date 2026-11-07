# Google Play Data safety checklist — verify before submission

This is a preparation checklist, not a declaration. Confirm actual SDK and server behavior before submitting.

- [ ] App functionality: Bluetooth device name/address and sensor readings.
- [ ] User-generated content: community post text, components and user photos.
- [ ] Account identifiers: Firebase Authentication UID.
- [ ] Device identifiers/diagnostics: disclose only if collected by enabled SDKs or server logs.
- [ ] Location: app does not intentionally request or use location; re-check Android permission and SDK behavior.
- [ ] Purchases: Google Play handles payment details; app receives product ID, purchase token/state through Play Billing.
- [ ] Data deletion: publish the hosted privacy policy and account-deletion URL; test callable deletion end-to-end.
- [ ] Review Firebase, Crashlytics/Analytics (if enabled), hosting logs and third-party SDK declarations.
