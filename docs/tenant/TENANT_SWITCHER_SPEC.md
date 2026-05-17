# Tenant Switcher Spec

Future multi-tenant users may switch between allowed workspaces.

Switcher requirements:

- list only tenants user belongs to
- never infer tenants from public data
- log tenant switch event
- clear active memory context when switching
