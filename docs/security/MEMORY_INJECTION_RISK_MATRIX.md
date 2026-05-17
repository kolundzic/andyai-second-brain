# Memory Injection Risk Matrix

| Risk | Description | Default action |
|---|---|---|
| Memory poisoning | Stored content tries to command future behavior | suspicious |
| Cross-session trigger | Dormant instruction activates later | suspicious |
| Tool escalation | Stored content asks for tool execution | action_blocked |
| Audit tamper | Content asks to hide or change logs | action_blocked |
| Public leakage | Content asks to publish private data | sensitive |
