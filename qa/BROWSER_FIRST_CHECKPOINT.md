# SalahPath browser-first checkpoint

This file marks the browser-first QA workflow as the primary development loop.

Rules:
- Validate current checked-in source in GitHub Actions on the iPhone simulator.
- Use targeted FAST screenshot runs during iteration.
- Use full `[de-qa]` screenshot coverage at checkpoints.
- Do not require physical iPhone testing until browser/simulator QA is clean.
- Physical-device-only checks remain Qibla sensor behavior, signing, notifications/background execution and final acceptance.
