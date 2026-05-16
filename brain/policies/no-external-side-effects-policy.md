# No External Side Effects Policy

The execution runtime is local-first. External side effects require explicit human approval.

Examples requiring approval:
- git push
- deployment
- deleting files outside repo scope
- sending emails/messages
- modifying production settings
