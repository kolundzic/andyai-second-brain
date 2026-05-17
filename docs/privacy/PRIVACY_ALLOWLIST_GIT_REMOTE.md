# Privacy Allowlist — Git Remote Metadata

## Reason

The privacy firewall correctly scans public artifacts, but it may classify Git remote metadata such as `git@github.com` as an email-like PII pattern.

That is a false positive when the string appears as Git SSH remote metadata, not as a personal email address.

## Rule

Allowlist only the exact Git remote metadata pattern:

```text
git@github.com
```

Do not allowlist arbitrary emails. Real email addresses must still be detected.

## Canon

Do not silence the alarm. Teach the alarm to distinguish smoke from fire.
