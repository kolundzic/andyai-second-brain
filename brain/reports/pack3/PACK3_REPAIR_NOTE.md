# PACK3 Repair Note

Original PACK3 stopped after v4.3.0 because the v4.4.0 action used an unescaped shell variable inside a strict-mode quoted eval string.

Repair policy:
- preserve successful tags v4.1.0 → v4.3.0
- continue from v4.4.0 → v6.0.0
- keep TAP-TAP v2 simplified UX
- keep local-first / push-later behavior
