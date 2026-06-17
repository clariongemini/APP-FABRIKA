> **Status:** experimental (not yet proven in production)

# Pattern: Chat App

## Intent

Threaded conversations with delivery state and optional realtime.

## When to use

- Messaging, support chat, AI chat UI

## Architecture checklist

- [ ] Message entity: id, thread_id, status (pending/sent/failed)
- [ ] Optimistic UI + rollback on failure
- [ ] Pagination (cursor-based)
- [ ] E2E optional — document threat model if not E2E
- [ ] Push for background (FCM) when not foreground

## Offline

- Outbox for unsent messages
- Sync on reconnect

## Anti-patterns

- Polling every N seconds on mobile
- Business logic in Composable lambdas
- Unbounded message list in memory

## Evidence

*(slug, retention D7, crash rate)*
