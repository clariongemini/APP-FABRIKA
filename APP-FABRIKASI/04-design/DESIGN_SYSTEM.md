# SVOS Design System Blueprint

World-class product UI — intentional, not AI-generated.

## Inspiration (principles only)

| Kaynak | Çıkarılan prensip |
|--------|-------------------|
| **Linear** | Density with clarity, keyboard-first, minimal chrome |
| **Stripe** | Typography hierarchy, trustworthy whitespace |
| **Notion** | Content-first, block mental model |
| **Figma** | Component consistency, design-dev parity |
| **Vercel** | Performance as UX, crisp borders |

## Token categories

```
color/       semantic (bg, fg, border, accent, danger)
typography/  scale, weight, line-height
spacing/     4px grid
radius/      sm, md, lg (restrained)
motion/      duration, easing (purposeful only)
elevation/   minimal — prefer border over shadow
```

## Hierarchy rules

1. One primary action per screen
2. Secondary actions visually subordinate
3. Data density matches user expertise (consumer vs pro)
4. Empty states teach, not decorate

## Interaction

- Feedback < 100ms perceived
- Destructive actions require confirmation
- Loading: skeleton > spinner > blank

## Accessibility

- WCAG 2.1 AA minimum (web)
- Dynamic type / font scaling (mobile)
- Focus visible always
- Color not sole information carrier

## Platform application

| Platform | Token location |
|----------|----------------|
| Android | `core/designsystem` (existing factory) |
| iOS | `Packages/CoreDesign/` (future) |
| Web | `styles/tokens/` (future) |

SVOS canonical tokens: [`tokens.yaml`](tokens.yaml) — platform adapters map to native.

## Anti-patterns

→ [`ANTI_PATTERNS.md`](ANTI_PATTERNS.md)
