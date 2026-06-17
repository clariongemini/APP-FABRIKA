# AI Platform Adapter

**Durum:** Blueprint only

## Target

- Agent workflows with phase separation
- Reasoning discipline (diagnostic vs implementation)
- Evaluation harnesses
- Memory systems (decision, pattern, venture context)
- Tool usage policies

## Principles (extracted, not copied)

From Cursor, Claude, Devin-class systems:

| Prensip | SVOS uygulaması |
|---------|-----------------|
| Context engineering | `10-runtime/context/` assembly |
| Validation gates | `01-core/governance/validation-gates.json` |
| Tool policies | Capability definitions in `03-agents/` |
| Phase separation | V0–V5 venture phases |
| Decision memory | `06-learning/adr/` |

**Yasak:** Leaked system prompts, vendor prompt archives.

## Components (future)

```
agents/           # Workflow definitions
evals/            # Regression eval sets
memory/           # Retrieval contracts
tools/            # Allowed tool surface
```

## Template

→ [`../../05-templates/ai-product/BLUEPRINT.md`](../../05-templates/ai-product/BLUEPRINT.md)
