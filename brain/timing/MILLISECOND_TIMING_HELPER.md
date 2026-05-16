# Millisecond Timing Helper

Use Python time in milliseconds for portable timing on macOS and Linux.

Avoid relying on `date +%s%3N`, because macOS date does not support GNU nanosecond formatting by default.
