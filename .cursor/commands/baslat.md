# /baslat — Projeyi Hiyerarşik Faz Planıyla Başlat

Geliştiricinin verdiği promptu **kod yazmadan önce** işle. Halüsinasyon sıfır; uydurma yasak.

## Girdi

Kullanıcının mesajındaki tüm metin = **kaynak prompt**. Ek argüman varsa onu da ekle.

## Zorunlu sıra

0. **Harici proje (AI Studio import):** `.factory/bootstrap_manifest.json` yoksa → önce `/import-aistudio` veya `bootstrap-external-project.sh` (bkz. `docs/AI_STUDIO_IMPORT.md`). Fabrika şablon reposunda bu adım atlanır.
1. **Skill:** `.cursor/skills/zero-hallucination/SKILL.md` uygula.
2. **Oku:** `docs/00-INDEX.md`, `.cursor/rules/00-overmind-zero-hallucination.mdc`
3. **YAPILACAKLAR oluştur/güncelle:**
   - `bash scripts/governance/init-yapilacaklar.sh "<prompt özeti>"`
   - Skill: `.cursor/skills/yapilacaklar-planner/SKILL.md`
4. Prompta göre **F1** ve **F7** tablolarına özel maddeler ekle (Ajan · L1 · Kabul · `bekliyor`).
5. **F0** fazını `işleniyor` bırak; F0.1'den başla — **henüz feature kodu yazma**.
6. `python3 scripts/governance/validate-yapilacaklar.py` çalıştır.

## F0 ilk adımlar (sırayla)

1. `./scripts/check-mcp.sh` — eksikse `docs/MCP_SETUP.md`
2. `./scripts/governance/init-governance.sh` (proje meta varsa)
3. F0 maddelerini tamamladıkça `tamamlandı` işaretle

## Çıktı formatı

```markdown
## YAPILACAKLAR oluşturuldu
- Aktif faz: F0
- Prompt kaydedildi: evet/hayır
- Eklenen özel maddeler: (liste)
- Sıradaki madde: F0.x — ...
- Blokör: (varsa)
```

## Yasak

- YAPILACAKLAR olmadan Kotlin/Gradle/UI üretmek
- F0 bitmeden F1'e geçmek
