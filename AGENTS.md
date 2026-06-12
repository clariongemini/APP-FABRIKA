# Ulas Autonomous Android APP Factory — Agent Directory

## 6 Departments / 6 Departman

| # | Agent | File | MCP Tools |
|---|-------|------|-----------|
| 1 | Product CPO | `01-product-cpo.mdc` | Browser, Fetch |
| 2 | Chief Architect | `02-architect.mdc` | GitHub, Docker |
| 3 | Android Elite | `03-android-elite.mdc` | — |
| 4 | Security Auditor | `04-auditor-security.mdc` | GitHub |
| 5 | OEM Auditor | `05-oem-compat-auditor.mdc` | Browser |
| 6 | MCP Orchestrator | `06-mcp-orchestrator.mdc` | All (setup) |

## First Session Protocol

```bash
./scripts/first-setup.sh    # MCP + health
./scripts/check-mcp.sh      # Verify P0 MCPs
```

See [docs/MCP_SETUP.md](docs/MCP_SETUP.md)

## Workflow

```
Mimar → Overmind → MCP Check → CPO → Architect → Android → Auditor → OEM Auditor → Mimar
```
