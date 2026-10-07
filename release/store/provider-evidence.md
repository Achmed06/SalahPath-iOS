# Quran provider privacy: evidence and unresolved scope

Reviewed on 7 October 2026. This is a preparation record, not a final App Privacy classification or legal assessment.

| Source | Confirmed published information | Limitation for SalahPath |
| --- | --- | --- |
| AlQuran.cloud terms | IP-based API rate limiting is described. | No complete Quran API/CDN request-log retention, linkage or deletion policy is established by these terms. |
| Islamic Network home/contact pages | The network identifies Mamluk as operator and Bahriya as host; its contact route points to the community and support tickets. | This identifies a route for clarification, not a final data-handling answer. |
| Bahriya Privacy Policy, updated 27 August 2026 | The hosting platform describes collection of platform access IPs and operational activity logs, with activity logs retained for up to 12 months. | The stated scope is the platform, console, API, website and related services. It does not explicitly map those retention periods to visitors of the hosted Quran API/CDN. Applying them directly would be an inference. |
| Bahriya HTTP Containers documentation | Gateway entries include request metadata and client IP. | The exact infrastructure used by each Quran endpoint and its retention settings are unconfirmed. |
| Islamic Network community discussion about `/timings/` | A respondent describes query-parameter logging and storage-dependent retention. | This concerns a different API. It is not sufficient evidence of current Quran API/CDN behavior. Its legal opinions are not adopted here. |

The new sources strengthen the reason to obtain endpoint-specific evidence. They do **not** resolve the outstanding App Store privacy answer. Do not declare "Data Not Collected", select a data category, or promise a retention period based solely on these leads.

No provider has been contacted during this task. `provider-privacy-request.txt` is ready for review but has not been sent.

## Sources

- https://alquran.cloud/terms-and-conditions
- https://islamic.network/
- https://islamic.network/contact.html
- https://bahriya.cloud/privacy
- https://bahriya.cloud/knowledgebase/containers/http-containers
- https://community.islamic.network/d/154-server-logs-log-retention-period

Kann Richtigkeit nicht garantieren – bitte verifizieren.
