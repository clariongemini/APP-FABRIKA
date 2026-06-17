# Template: ai-product

## Architecture blueprint

- Agent workflow + eval harness
- Memory: venture context + decision ADR
- Ref: `02-platforms/ai/ADAPTER.md`

## Launch checklist

- [ ] V0 charter + safety boundaries
- [ ] Eval set baseline
- [ ] Human-in-the-loop for high-risk actions
- [ ] Rate limits + abuse prevention

## Analytics plan

- Task completion rate
- User correction rate
- Latency p95

## Testing plan

- Eval regression before each release
- Red-team prompt set (internal)

## Release plan

- Internal dogfood → limited beta → GA with monitoring
