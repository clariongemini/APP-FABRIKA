> **Status:** experimental (not yet proven in production)

# Pattern: Media App

## Intent

Audio/video playback with background, cache, and OEM battery constraints.

## When to use

- Players, podcasts, offline media libraries

## Architecture checklist

- [ ] ExoPlayer / Media3 in dedicated module
- [ ] Foreground service + notification channel (OEM)
- [ ] Cache policy: size cap, eviction, offline download queue
- [ ] Audio focus and Bluetooth route handling
- [ ] Metadata separate from binary storage

## Performance

- Cold start: defer heavy codec init
- `docs/03-STANDARDS/PERFORMANCE.md` — battery, memory

## OEM

- Samsung / MIUI background kill — `05-oem-compat-auditor.mdc`
- Battery optimization whitelist UX (consent-based)

## Anti-patterns

- Parsing metadata in UI thread
- Unbounded disk cache
- yt-dlp or scrape-dependent core flows without legal review

## Evidence

*(Failures often land in knowledge/failures/ — link here)*
