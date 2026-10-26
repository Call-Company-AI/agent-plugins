# Directory submission preparation

Package publication, hosted connection verification, directory review, and directory publication are separate checkpoints. A successful local check or public repository does not mean a directory approved the plugin.

## Shared listing

| Field | Value |
| --- | --- |
| Display name | Call Company |
| Publisher | Call Company AI |
| Repository | https://github.com/Call-Company-AI/agent-plugins |
| Plugin path | Repository root (`.`) |
| MCP URL | https://api.callcompany.ai/api/mcp |
| Transport | Streamable HTTP |
| Authentication | OAuth with dynamic client registration and PKCE |
| Call Company plan | Pro or higher for hosted MCP |
| Documentation | https://github.com/Call-Company-AI/agent-plugins#readme |
| Website | https://www.callcompany.ai |
| Support | https://www.callcompany.ai/contact |
| Privacy | https://www.callcompany.ai/privacy |
| Terms | https://www.callcompany.ai/terms |
| Icon | `assets/logo.png`, 512 × 512 PNG |

Short description: **Run your AI phone agents**

Description:

> Review calls, check agent readiness, keep knowledge current, and prepare, test and publish agent configuration changes. Sign in to Call Company and approve access to your Organization. Configuration edits remain drafts until published; other actions have the effects described by their tools. Available actions depend on your role and approved permissions.

Keep plan requirements in setup documentation and reviewer instructions. OpenAI's public listing must not advertise plans or upgrades; use the description above and the packaged metadata.

## Claude

1. Validate the repository root with `claude plugin validate . --strict`.
2. Use the [directory portal](https://claude.ai/directory/manage) to prepare the remote MCP connector and the GitHub plugin bundle, following the portal's current workflow. Select this repository and the root plugin path.
3. Use the shared listing details and run the reviewer scenarios against a dedicated account.
4. Complete required tool review, data-handling declarations, reviewer access and any separate connector linking requested by the portal.
5. Submit only after the actual results support the attestations. Approval and publication are subsequent steps.

See [Claude submission](https://claude.com/docs/plugins/submit) and the [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).

## ChatGPT and Codex

1. Run `python3 scripts/package.py`; upload `dist/callcompany-chatgpt.zip` in [OpenAI Platform → Plugins](https://platform.openai.com/plugins).
2. Choose the verified Call Company publishing identity and the remote **With MCP** route. Confirm the portal detects OAuth and dynamic client registration from the hosted endpoint. The portable package uses the canonical Agent Plugins schema; authentication is advertised by the server.
3. Complete the portal's domain-verification challenge, authenticate, and inspect the current tool scan. A configured challenge handler does not itself prove domain ownership was verified.
4. The ZIP supplies five positive and three negative review scenarios. Run them using the dedicated reviewer account, record actual results, and provide an accessible video walkthrough.
5. Enter reviewer credentials only in the secure portal. Resolve automated findings before accepting attestations and submitting. Publish after approval.

See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission), and [remote MCP review](https://developers.openai.com/plugins/deploy/app-review).

## Reviewer account and demo

Use a dedicated Pro-or-higher account and Organization with synthetic business data, a representative agent and draft, knowledge, and recent synthetic call records. Do not give reviewers access to customer Organizations. Keep the account usable for re-review and use the authentication method the directory supports. Credentials, grant IDs, customer data, and account-specific evidence must never be committed or included in an archive.

Review scenarios are in `plugin.json` under `extensions.com.openai.review.test_cases`. The call-summary case asks “Summarize my two most recent calls.” Create two clearly labeled synthetic records through the supported fixture path using its normal timestamps; no backdating or daily refresh is needed. Before recording, use `list_calls` with `limit: 2` and `get_call` for each returned ID to verify their actual order, caller requests, and outcomes. The list is Organization-scoped; do not invent an agent filter. Follow `next_cursor` only if a smaller page requires it to reach two calls, and report fewer records or unavailable details truthfully. Record a walkthrough of connection, readiness, call summaries, one call read, a knowledge update, and a greeting draft edit. Show the saved result and distinguish it from publication. Run the negative cases and verify that unrelated requests do not invoke Call Company tools. Use a disposable review agent for writes; a recording must show real outcomes, not scripted claims.

Before final submission, verify the production tool metadata, full OAuth connection, representative authorized reads and writes, permission denials, revocation, privacy disclosures, public links, reviewer login, video, and publisher identity. Keep an explicit list of items not yet verified; do not mark them passed from code inspection alone.

After a developer-tier release, record both Pro MCP success and direct API refusal, Business API success, Starter refusal, downgrade, and revoked-token refusal. Never claim that a marketplace listing unlocks a lower Call Company plan.
