# Template: android-app

## Architecture blueprint

- 10-module Gradle (app + 7 core + 3 feature)
- Offline-first · Room · Hilt · Compose
- Ref: `02-platforms/android/ADAPTER.md`

## Launch checklist

- [ ] V0 charter approved
- [ ] `init-new-app.sh` executed
- [ ] i18n tr + en
- [ ] Play Console listing draft
- [ ] Privacy policy URL
- [ ] OEM matrix reviewed (if background work)

## Analytics plan

- Sprint P minimum events (session, feature_use, error)
- Firebase or equivalent
- Crashlytics

## Testing plan

- Unit: domain + use cases
- Integration: Room, billing stub
- Manual: OEM devices (Samsung, Xiaomi if applicable)

## Release plan

- Internal test → closed beta → production staged (10% → 100%)
