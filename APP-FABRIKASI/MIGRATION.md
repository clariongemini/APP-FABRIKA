# Migration Path — Standalone APP-FABRIKA Repository

## Mevcut durum (2026-06-14)

| Repo | Rol |
|------|-----|
| [clariongemini/Android-App](https://github.com/clariongemini/Android-App) | Frozen Android Factory template (v3.1) |
| [clariongemini/APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) | **Canonical** — SVOS + Android Factory monorepo |

## Faz 1 — Monorepo (şimdi)

```
APP-FABRIKA/
├── APP-FABRIKASI/          # SVOS çekirdeği (yeni)
├── templates/android/      # Android adapter impl
├── governance/             # Geçiş — Android Factory
├── knowledge/              # Geçiş — Learning Factory
├── scripts/                # Android tooling
└── ...
```

Android Factory **operasyonel ve dokunulmaz**. SVOS üst katman olarak eklenir.

## Faz 2 — Venture isolation (ilk ship sonrası)

Her venture ayrı repo veya workspace:

```bash
git clone https://github.com/clariongemini/APP-FABRIKA.git my-venture
cd my-venture
./scripts/init-new-app.sh "My Venture" "com.company.app"
# SVOS charter: APP-FABRIKASI/08-ventures/my-venture/
```

Venture repo'su `sync-standards.sh` ile fabrikadan güncellenir.

## Faz 3 — SVOS extraction (3+ ventures, 3+ outcomes)

| Taşınacak | Hedef |
|-----------|-------|
| `APP-FABRIKASI/01-core` | Standalone `svos-core` package |
| `APP-FABRIKASI/06-10` | Standalone repo |
| Android impl | Kalır veya `android-adapter` submodule |

Trigger: `.factory/freeze.json` `until_apps_released: 3` benzeri SVOS kriteri.

## Faz 4 — Platform adapter repos (opsiyonel)

```
svos-core          # governance + learning + intelligence
adapter-android    # fork/sync from templates/android
adapter-ios
adapter-web
```

## Git remote stratejisi

```bash
git remote rename origin android-app   # eski (opsiyonel archive)
git remote add origin https://github.com/clariongemini/APP-FABRIKA.git
git push -u origin main
```

## Veri migrasyonu

| Kaynak | Hedef | Yöntem |
|--------|-------|--------|
| `knowledge/*` | `APP-FABRIKASI/06-learning/` | Copy-on-venture, not bulk move |
| `governance/executive/*` | Referans only | Android Factory frozen |
| Outcomes | `08-ventures` + `07-evidence` | Per venture on ship |

## Başarı kriteri

Migration tamam sayılır when:
- APP-FABRIKA canonical remote
- ≥1 venture shipped with evidence loop
- Android Factory CI still green
- No duplicate governance trees
