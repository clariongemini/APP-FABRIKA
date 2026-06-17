# Core Runtime Contracts

SVOS runtime path sözleşmeleri. Gerçek veri `10-runtime/` altında (gitignore ile venture-specific).

## Path şeması

```
10-runtime/
├── context/           # Assembled context manifests
├── ventures/          # Active venture state
├── evidence-index/    # Evidence lookup index (no raw PII in git)
└── cache/             # Ephemeral (gitignored)
```

## Assembly sırası

1. Venture charter (08-ventures)
2. Platform adapter standards (02-platforms)
3. Proven patterns (06-learning)
4. Recent evidence summary (07-evidence)
5. Portfolio context if N≥2 ventures (09-portfolio)

Token bütçesi: özet önce, tam dosya talep üzerine.
