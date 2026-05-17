# Homepage Upload Nav Link Patch

## Problem

PACK44 created the `/upload/` route, but the homepage top navigation did not expose the Upload link.

## Fix

`v88.0.4` adds the Upload link to the homepage navigation and relevant generator/runtime files so the link is preserved after rebuilds.

## Route

```text
/upload/
```

## Rule

A public prototype route must be reachable from the main navigation once it becomes part of the product story.
