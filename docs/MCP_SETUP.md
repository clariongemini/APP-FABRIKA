# MCP Kurulum Kılavuzu / MCP Setup Guide

## Türkçe

### Neden MCP?

Fabrika ajanları (CPO, Baş Mimar, Denetçi) tek başına sınırlıdır. **MCP (Model Context Protocol)** sunucuları ajanlara gerçek dünya yetenekleri kazandırır:

| MCP | Ajan | Görev |
|-----|------|-------|
| **Browser** | CPO | Rakip analizi, Play Store, pazar araştırması |
| **GitHub** | Baş Mimar, Denetçi | Repo, CI, PR, release |
| **Docker** | Baş Mimar | İzole build ortamı |
| **GitKraken** | Tümü | Git işlemleri, code review |
| **Fetch** | CPO | Web içerik çekme |

### İlk Kurulum (Zorunlu)

```bash
./scripts/first-setup.sh
```

Bu script:
1. MCP kurulumunu kontrol eder
2. Eksik MCP'leri raporlar
3. Git hook + fabrika sağlık testini çalıştırır

### Cursor'da MCP Ekleme

1. **Cursor** → **Settings** → **MCP** → **Add new MCP server**
2. Proje kökündeki `.cursor/mcp.json.example` dosyasını `.cursor/mcp.json` olarak kopyala
3. `GITHUB_PERSONAL_ACCESS_TOKEN` değerini gir ([GitHub PAT oluştur](https://github.com/settings/tokens) — `repo` scope)
4. **cursor-ide-browser**: Cursor ile birlikte gelir — MCP listesinde etkinleştir

### Overmind Talimatı

İlk oturumda Cursor ajanı şunu yapmalı:
1. `./scripts/check-mcp.sh` çalıştır
2. P0 MCP eksikse → `docs/MCP_SETUP.md` oku ve kullanıcıya kurulum adımlarını sun
3. Kurulum tamamlanana kadar kod üretimine **başlama** (CPO pazar araştırması hariç yerel belgelerle)

### Doğrulama

```bash
./scripts/check-mcp.sh
```

---

## English

### Why MCP?

Factory agents (CPO, Architect, Auditor) have limits alone. **MCP servers** give agents real-world capabilities:

| MCP | Agent | Task |
|-----|-------|------|
| **Browser** | CPO | Competitor analysis, Play Store research |
| **GitHub** | Architect, Auditor | Repo, CI, PR, releases |
| **Docker** | Architect | Isolated Gradle builds |
| **GitKraken** | All | Git ops, code review |
| **Fetch** | CPO | Web content retrieval |

### First Setup (Required)

```bash
./scripts/first-setup.sh
```

### Add MCP in Cursor

1. **Cursor** → **Settings** → **MCP** → **Add new MCP server**
2. Copy `.cursor/mcp.json.example` → `.cursor/mcp.json`
3. Set `GITHUB_PERSONAL_ACCESS_TOKEN` ([create PAT](https://github.com/settings/tokens))
4. Enable **cursor-ide-browser** in MCP list

### Overmind Protocol

On first session, the agent must:
1. Run `./scripts/check-mcp.sh`
2. If P0 MCPs missing → guide user through `docs/MCP_SETUP.md`
3. Do not start code generation until MCP setup is complete (except local doc work)

### Verify

```bash
./scripts/check-mcp.sh
```
