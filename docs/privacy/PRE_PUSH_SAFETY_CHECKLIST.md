# Pre-Push Safety Checklist

Before `git push`:

- Run `runtime/bin/privacy-firewall public-gate`
- Run `runtime/bin/privacy-firewall audit`
- Confirm no real client data is staged
- Confirm no secrets are staged
- Confirm all client reports are approved
- Confirm public output is redacted or synthetic
