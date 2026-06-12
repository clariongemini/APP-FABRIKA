# Bootstrap Kılavuzu — Yeni Android Projesi Başlatma

Bu belge, Autonomous App Factory'yi yeni bir Android projesine nasıl uygulayacağınızı adım adım açıklar.

## Senaryo A: GitHub Template ile Sıfırdan

1. GitHub'da **Ulas Autonomous Android APP Factory** → **Use this template**
2. Klonla ve Cursor'da aç
3. İlk kurulum:

```bash
./scripts/first-setup.sh
```

4. MCP kurulumu (zorunlu): `docs/MCP_SETUP.md`
5. Uygulama oluştur:

```bash
./scripts/init-new-app.sh "UygulamaAdi" "com.sirket.uygulama"
```

4. `init-new-app.sh` otomatik olarak:
   - Tüm belgeleri oluşturur
   - **Tam Android iskeletini** scaffold eder (10 modül)
5. Cursor chat'te:

```
Bu projeyi 33 katman standartlarına göre geliştir.
Uygulama: [kısa açıklama]
```

Overmind `docs/00-INDEX.md` okur, CPO ajanı pazar analizine başlar.

## Senaryo B: Mevcut Android Projesine Standart Aktarma

```bash
# Fabrika reposunu bir kez klonla
git clone https://github.com/YOUR_ORG/autonomous-app-factory.git ~/autonomous-app-factory

# Mevcut projene standartları aktar
export FACTORY_REPO=~/autonomous-app-factory
cd /path/to/mevcut-proje
$FACTORY_REPO/scripts/sync-standards.sh .
```

Aktarılan içerik:
- `.cursorrules`
- `.cursor/rules/*.mdc`
- `docs/` (standart belgeler + şablonlar)
- `scripts/` (denetim araçları)

Mevcut `app/` kodunuz korunur. Sadece AI kuralları ve dokümantasyon eklenir.

## Senaryo C: Git Submodule (Güncel Standart Takibi)

```bash
cd my-android-app
git submodule add https://github.com/YOUR_ORG/autonomous-app-factory.git .factory

# Standartları senkronize et
./.factory/scripts/sync-standards.sh .

# Fabrika güncellendiğinde
git submodule update --remote .factory
./.factory/scripts/sync-standards.sh .
```

## init-new-app.sh Ne Yapar?

| Adım | Açıklama |
|------|----------|
| 1 | `docs/00-INDEX.md` içine uygulama adı ve paket adı yazar |
| 2 | `docs/01-VISION/` altına şablon brifler oluşturur |
| 3 | `docs/02-ARCHITECTURE/MODULE_MAP.md` şablonunu oluşturur |
| 4 | `docs/TODO.md` sıfırlar ve Faz 0 ekler |
| 5 | `android/` klasör yapısı referansını oluşturur |

## Cursor'da Kullanım İpuçları

- **İlk prompt:** Uygulama fikrini verin, kod istemeyin — Overmind önce vizyon belgelerini oluşturur
- **Devam promptu:** `@docs/00-INDEX.md` ile hafızayı tazeleyin
- **Denetim:** Kod yazıldıktan sonra `./scripts/pre-commit.sh` çalıştırın
- **Katman kontrolü:** `./scripts/audit-layers.sh`

## GitHub Template Ayarı

Repo sahibi GitHub'da şunu yapmalı:

1. **Settings** → **General** → **Template repository** ✅ işaretle
2. README'deki `YOUR_ORG` placeholder'ını gerçek org/ad ile değiştir

## Sık Sorulan Sorular

**Her projede fabrika reposunu fork'lamalı mıyım?**  
Hayır. Template kullanın veya `sync-standards.sh` ile mevcut projeye aktarın.

**Standartlar güncellenirse ne olur?**  
Submodule veya `sync-standards.sh` ile yeniden senkronize edin. `CHANGELOG.md` değişiklikleri takip edin.

**Android kodu bu repoda mı?**  
Hayır. Bu repo standartların kaynağıdır. Uygulama kodu template'den türeyen proje reposunda yaşar.
