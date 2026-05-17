# v66.0.2 — Privacy Allowlist / Git Remote False Positive Cleanup

This narrow repair updates the privacy firewall so `git@github.com` Git remote metadata is not treated as a PII leak in public artifacts.

The R2 repair also fixes `rel(path)` so scanner reports do not crash when a future diagnostic scans a temporary file outside the repository.

The fix is intentionally narrow:

- `git@github.com` is allowlisted.
- Normal email addresses are still detected.
- Public gate remains active.
- Vercel deploy still requires human approval.
