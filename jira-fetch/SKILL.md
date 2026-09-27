---
name: jira-fetch
description: Connect to Jira and fetch an issue's details by pasting a Jira issue URL or an issue key (e.g. PROJ-123). Reads the Jira domain and credentials from .claude/.env, calls the Jira REST API (Cloud v3 or Server/DC v2) with stdlib-only Python, and returns a readable summary (type, status, assignee, description, attachments, optionally comments). Can also download the issue's attachments (screenshots, logs, PDFs) to disk so they can be opened and analysed alongside the description. Use when the user pastes a Jira link or issue key, or says "get the Jira issue", "lấy thông tin Jira", "xem ticket Jira", "lấy cả file đính kèm", "what's in PROJ-123", "jira-fetch".
argument-hint: "<Jira issue URL or key, e.g. PROJ-123>"
---

# Jira Fetch — issue lookup by URL or key

Pulls a Jira issue's details from the Jira REST API given either a **full Jira URL**
(`https://your-company.atlassian.net/browse/PROJ-123`) or just an **issue key**
(`PROJ-123`). All connection settings live in [`.claude/.env`](../../.env) — never
hard-code them and never echo the token.

## Config contract (`.claude/.env`)

| Key | Required | Meaning |
|-----|----------|---------|
| `JIRA_DOMAIN` | yes* | host only, no scheme — e.g. `your-company.atlassian.net` |
| `JIRA_EMAIL` | for basic | account email (Jira Cloud / Basic auth) |
| `JIRA_API_TOKEN` | yes | API token (Cloud) or Personal Access Token (Server/DC) |
| `JIRA_AUTH_TYPE` | no | `basic` (default, Cloud) or `bearer` (Server/DC PAT) |
| `JIRA_API_VERSION` | no | `3` (default, Cloud) or `2` (Server/DC) |

\* If the user pastes a full URL, its host overrides `JIRA_DOMAIN`, so a key-only
config still works across multiple Jira sites.

- **Jira Server/DC** (e.g. `jira.fci.vn`): there is no `id.atlassian.com` token
  page. Use `JIRA_API_VERSION=2` and either a **Personal Access Token** (avatar →
  Profile → "Personal Access Tokens" → Create; set `JIRA_AUTH_TYPE=bearer`,
  `JIRA_API_TOKEN=<PAT>`) or, on older Jira, **username + password**
  (`JIRA_AUTH_TYPE=basic`, `JIRA_EMAIL=<username>`, `JIRA_API_TOKEN=<password>`).
- **Jira Cloud**: token at <https://id.atlassian.com/manage-profile/security/api-tokens>
  (`JIRA_AUTH_TYPE=basic`, `JIRA_API_VERSION=3`, `JIRA_EMAIL` = account email).
- `.claude/.env` holds a real secret → it MUST stay git-ignored (already added to
  `.gitignore`). Never print `JIRA_API_TOKEN`.

## Process

1. **Read the input.** Take the URL or key the user gave. If neither was provided,
   ask for one (or for the key). Do not guess a key.
2. **Verify config exists.** If [`.claude/.env`](../../.env) lacks `JIRA_DOMAIN` /
   `JIRA_API_TOKEN` (still the placeholder), tell the user which keys to fill in
   per the table above and stop — don't invent credentials.
3. **Run the fetcher** from the project root:

   ```bash
   python .claude/skills/jira-fetch/scripts/jira_fetch.py "<url-or-key>"
   ```

   Useful flags:
   - `--comments` — also fetch and print the issue's comments.
   - `--download-attachments [DIR]` — download the issue's attachments to disk so
     they can be opened and analysed. Without `DIR` they land in
     `./jira-attachments/<KEY>/`; pass a dir (e.g. the scratchpad) to override.
   - `--raw` — print the raw JSON (use when the user needs custom fields).
   - `--env PATH` — point at a different `.env` (auto-detected otherwise).

   The script extracts the key, picks Basic vs Bearer auth, calls
   `/rest/api/{version}/issue/{key}`, flattens the description (handles both the
   ADF JSON of Cloud v3 and plain text of Server v2), and prints a Markdown summary.
   The summary **always** lists the issue's attachments (name, size, type); with
   `--download-attachments` each saved file's local path is shown too.

4. **Fetch attachments when they matter.** If the issue has attachments and the
   user wants them (or the task is a bug analysis / anything where a screenshot,
   log, or PDF would clarify the problem), re-run with
   `--download-attachments "<dir>"` (prefer the session scratchpad dir). The files
   authenticate via the same token — no separate step. Then **open each relevant
   attachment with the Read tool** (images and PDFs render visually; logs/text read
   as-is) and analyse it **together with the Description** — e.g. read the error in
   a screenshot, the stack trace in an attached log, or the mockup in a PDF.

5. **Relay the result.** Present the summary to the user, incorporating what the
   attachments show. On an HTTP error the script prints a diagnostic (401/403 =
   token/permission, 404 = wrong key/domain) — surface that and suggest the likely
   fix; do not retry blindly with a changed token unless the user provides one.

## Notes

- Stdlib only (`urllib`) — no `pip install` needed; runs on the project's Python.
- Read-only **on Jira**: this skill never edits, transitions, or comments on issues.
  `--download-attachments` only writes downloaded files locally (into the given DIR
  or `./jira-attachments/<KEY>/`); attachment names are sanitised so they can't
  escape that directory.
- For repeated lookups in one turn, call the script once per key rather than
  re-asking for config.
