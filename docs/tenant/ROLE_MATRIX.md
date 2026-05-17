# Role Matrix

| Role | Purpose | Allowed direction |
|---|---|---|
| owner | controls tenant and billing | manage workspace, approve high-risk actions |
| admin | manages users/workflows | manage workspace operations |
| operator | runs TAP-TAP/operator tasks | execute approved workflows |
| member | uses personal workspace features | ask/upload/search own allowed data |
| viewer | read-only access | view approved artifacts only |

Rule: service-role operations are never user-role operations.
