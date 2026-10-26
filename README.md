# Call Company

Connect Claude, ChatGPT, Codex, and other MCP clients to your [Call Company](https://www.callcompany.ai) account. Review calls, update knowledge, check agent readiness, and prepare, test, and publish changes to your AI phone agents.

This repository contains connection settings and a workflow skill. Call Company's backend remains hosted; this package does not run a local server. A Call Company account on **Pro or higher** is required for this hosted MCP connection. Direct public API and SDK access require **Business or higher**; customer webhooks require **Pro or higher**. Available tools also depend on your Organization, role, and approved permissions.

## Connect

The production MCP URL is:

```text
https://api.callcompany.ai/api/mcp
```

Use Streamable HTTP with OAuth. Sign in on the Call Company page and review the requested permissions. Never paste an API key, password, or access token into a conversation or commit it to this repository.

### Claude

In Claude, add a custom remote connector with the URL above, then connect your account. See [Claude's custom connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

In Claude Code, install the workflow skill and connection together:

```text
/plugin marketplace add Call-Company-AI/agent-plugins
/plugin install callcompany@callcompany
```

Run `/mcp`, select `callcompany`, and authenticate when prompted. For an MCP-only connection instead:

```sh
claude mcp add --transport http callcompany https://api.callcompany.ai/api/mcp
```

### ChatGPT and Codex

The public directory packages are being prepared; this repository does not imply directory approval. For supported custom MCP connections, use the URL above and OAuth. ChatGPT custom connections depend on your plan and workspace settings; follow [OpenAI's connection guide](https://developers.openai.com/plugins/deploy/connect-chatgpt).

In Codex CLI, connect directly:

```sh
codex mcp add callcompany --url https://api.callcompany.ai/api/mcp
codex mcp login callcompany
```

The root `plugin.json`, `mcp.json`, and `skills/` also form the portable package for ChatGPT and Codex. Maintainers can generate an uploadable ZIP using the command below.

## Try it

- “Which of my agents are ready to take calls?”
- “Summarize this week's calls for my front desk agent.”
- “Change my agent's greeting to ‘Welcome to Bella Vista. How can I help?’”

Agent configuration edits remain drafts until published. Other writes can have immediate effects; the assistant should explain the particular action and follow your authorization. The included skill requires explicit instructions for publication, rollback, phone changes, and other consequential actions. Server permissions remain authoritative.

## Data and access

Authorized tool results may include agent configuration, knowledge, call records, and transcripts. They travel between Call Company's servers and the assistant provider you connect. Share only the data needed for your request. Disconnect or revoke access in Call Company → Settings → AI assistants. A downgrade pauses developer runtime access; existing credentials do not bypass the current plan. Configuration and revocation remain available. If your billing screen does not offer Pro or Business, contact support for help moving from a legacy plan.

[Privacy](https://www.callcompany.ai/privacy) · [Terms](https://www.callcompany.ai/terms) · [Support](https://www.callcompany.ai/contact) · [Connector documentation](https://app.callcompany.ai/docs/mcp-access)

## Maintain and package

Python 3.10+ is sufficient; packaging has no third-party dependencies.

```sh
python3 scripts/package.py --check
python3 scripts/package.py
claude plugin validate . --strict
```

This creates reproducible `dist/callcompany-chatgpt.zip` and `dist/callcompany-claude.zip` archives using explicit file lists. See [submission preparation](https://github.com/Call-Company-AI/agent-plugins/blob/main/docs/submissions.md). Reviewer credentials and account-specific evidence belong outside this public repository and its ZIPs.

The package code and documentation use the [ISC license](LICENSE). Call Company names and branding remain their owners' property; see [branding](assets/README.md).
