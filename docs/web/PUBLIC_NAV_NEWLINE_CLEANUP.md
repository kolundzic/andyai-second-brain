# Public Nav Escaped Newline Cleanup

## Problem

A literal `\n` appeared in the public homepage navigation between `Health` and `Help`.

Visible symptom:

```text
Health \n Help
```

## Cause

A previous patch inserted escaped newline text into generated HTML instead of a real newline.

## Fix

`v82.0.2` cleans the rendered public HTML and generator sources so the public menu renders cleanly.

## Rule

Public navigation must not display escaped control characters.
