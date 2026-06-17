# iOS Platform Adapter

**Durum:** Blueprint only

## Target stack

- Swift 5.9+
- SwiftUI + Observation
- SPM modular layout
- Offline-first default (SwiftData / Core Data)
- XCTest + UI tests on critical paths

## Proposed module shape

```
App/
Packages/
  CoreCommon/
  CoreDesign/
  CoreData/
  CoreNetwork/
  FeatureHome/
  FeatureSettings/
```

## Standards (summary)

| Alan | Hedef |
|------|-------|
| Architecture | MVVM + Clean boundaries |
| UI | Native HIG, adaptive iPhone/iPad |
| Security | Keychain, App Attest (V2) |
| Release | TestFlight → App Store staged |

## Validation (future)

- `xcodebuild` CI
- SwiftLint
- Architecture test package

## Template

→ [`../../05-templates/ios-app/BLUEPRINT.md`](../../05-templates/ios-app/BLUEPRINT.md)
