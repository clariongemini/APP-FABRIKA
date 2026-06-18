# Enterprise Design Principles

SVOS ventures (Web, iOS, Android) must feel **intentional** — not AI-generated.

Reference quality bar: Linear, Notion, Stripe, Apple HIG — **principles only**, no component library.

Tokens: [`../04-design/tokens.yaml`](../04-design/tokens.yaml) · Anti-patterns: [`../04-design/ANTI_PATTERNS.md`](../04-design/ANTI_PATTERNS.md)

---

## Typography

| Rule | Web | iOS |
|------|-----|-----|
| Scale | 12/14/16/18/24/32 — max 6 sizes | Dynamic Type — never block scaling |
| Family | One sans + one mono | SF Pro / system |
| Weight | 400 body, 600 headings only | Regular/Medium/Semibold |
| Line height | 1.5 body, 1.2 headings | Apple text styles |
| **Reject** | Inter + purple gradient hero | Rounded bubble UI everywhere |

One typographic voice per venture. No mixing 3+ families.

---

## Spacing

- Base unit: **4px** (8pt on iOS)
- Layout rhythm: 8, 16, 24, 32, 48 — no arbitrary 13px gaps
- Content max-width web: 640–1120px by context
- Touch targets: **44×44pt** minimum (iOS), 48dp (Android)
- Whitespace is structure — dense ≠ professional

---

## Interaction

- One primary action per screen
- Destructive actions: confirm + reversible when possible
- Loading: skeleton > spinner > blank
- Errors: what happened + what to do — never raw codes to users
- Forms: inline validation, preserve input on failure
- Navigation: predictable back — no mystery gestures as only exit

Stripe rule: **every click earns its place.**

---

## Motion

| Use | Avoid |
|-----|-------|
| State change (open/close) | Decorative loops |
| 150–250ms default | >400ms blocking |
| Ease-out enter, ease-in exit | Bounce on every element |
| Reduced motion respect | Parallax by default |

Motion communicates **state**, not decoration.

---

## Accessibility

- WCAG 2.1 AA minimum (web)
- VoiceOver / TalkBack labels on all controls
- Color never sole signal — icon + text
- Focus order logical (web keyboard)
- Contrast 4.5:1 body text
- iOS: Dynamic Type, Bold Text, Reduce Motion

---

## Anti-AI patterns (mandatory rejection)

| Pattern | Why |
|---------|-----|
| Purple/blue gradient hero | Instant "AI slop" |
| Glassmorphism stacks | Readability loss |
| Generic illustration packs | No brand memory |
| Centered everything | No hierarchy |
| Emoji as icons | Unprofessional |
| "Dashboard" as home | Metrics ≠ user job |
| Card grid of 12 equal widgets | No priority |
| Lorem or filler copy in ship | Trust destroyer |
| Rounded-3xl on everything | Template look |

**ux** capability signs off using this doc before release gate.

---

## Platform notes

### Web
- Semantic HTML first
- CSS variables from tokens.yaml
- No inline style soup in generated code

### iOS
- HIG layout margins
- Native navigation patterns (tab bar, nav stack)
- SF Symbols — consistent weight

### Android (reference)
- Material 3 with venture accent only
- Compose — see factory Liquid Glass standard

---

## Review checklist (ux capability)

- [ ] ≤6 type sizes used
- [ ] Spacing on 4px grid
- [ ] One clear primary CTA
- [ ] No anti-AI patterns
- [ ] a11y pass on target platform
- [ ] Motion respects reduced-motion
