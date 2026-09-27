#!/usr/bin/env python3
"""Fetch a Jira issue by key or URL using only the Python standard library.

Reads connection config from .claude/.env (see SKILL.md for the contract):

    JIRA_DOMAIN       your-company.atlassian.net   (no scheme, no trailing slash)
    JIRA_EMAIL        you@company.com              (Cloud / Basic auth)
    JIRA_API_TOKEN    <api token or PAT>
    JIRA_AUTH_TYPE    basic | bearer               (optional, default: basic)
    JIRA_API_VERSION  3 | 2                        (optional, default: 3 = Cloud)

Usage:
    python jira_fetch.py <issue-key-or-url> [--comments] [--raw] [--env PATH]
                         [--download-attachments [DIR]]

The script:
  * accepts a bare key (PROJ-123), a browse URL, or a REST URL and extracts the key
  * authenticates with Basic (email:token) or Bearer (PAT)
  * prints a readable summary, or full JSON with --raw
  * always lists the issue's attachments (name, size, type) in the summary
  * with --download-attachments, saves each attachment to disk so the caller can
    open/analyse it (e.g. read a screenshot or a log referenced by the bug)
  * never echoes the token; auth failures are reported without leaking secrets
"""
import argparse
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

# Matches PROJECT-123 anywhere; PROJECT key is 1+ letters/digits starting with a letter.
ISSUE_KEY_RE = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b", re.IGNORECASE)


def find_env_file(explicit):
    """Locate .env file, walking up from cwd or checking standard global locations."""
    if explicit:
        return explicit
    here = os.path.abspath(os.getcwd())
    while True:
        for rel in [os.path.join(".claude", ".env"), ".env.dev", ".env.local", ".env"]:
            candidate = os.path.join(here, rel)
            if os.path.isfile(candidate):
                return candidate
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    # Fallback to home/global locations
    for global_path in [
        os.path.expanduser("~/.claude/.env"),
        os.path.expanduser("~/.gemini/.env"),
        os.path.expanduser("~/.gemini/config/.env"),
    ]:
        if os.path.isfile(global_path):
            return global_path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "..", ".env"))


def load_env(path):
    """Minimal .env parser: KEY=VALUE lines, ignores comments/blank, strips quotes."""
    env = {}
    if not os.path.isfile(path):
        return env
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                env[key] = value
    return env


def extract_issue_key(text):
    """Pull a PROJ-123 key out of a bare key, browse URL, or REST URL."""
    text = text.strip()
    match = ISSUE_KEY_RE.search(text)
    if match:
        return match.group(1).upper()
    return None


def domain_from_input(text):
    """If the input is a full URL, return its host so it can override JIRA_DOMAIN."""
    if "://" in text:
        parsed = urllib.parse.urlparse(text)
        return parsed.netloc or None
    return None


def build_auth_header(env):
    auth_type = (env.get("JIRA_AUTH_TYPE") or "basic").strip().lower()
    token = env.get("JIRA_API_TOKEN", "").strip()
    if not token:
        raise SystemExit("ERROR: JIRA_API_TOKEN is not set in .claude/.env")
    if auth_type == "bearer":
        return f"Bearer {token}"
    email = env.get("JIRA_EMAIL", "").strip()
    if not email:
        raise SystemExit("ERROR: JIRA_EMAIL is required for basic auth in .claude/.env")
    raw = f"{email}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def fetch_issue(domain, version, key, auth_header, with_comments):
    fields = (
        "summary,status,issuetype,priority,assignee,reporter,created,updated,"
        "labels,components,fixVersions,parent,resolution,description,attachment"
    )
    query = {"fields": fields, "expand": "renderedFields"}
    url = f"https://{domain}/rest/api/{version}/issue/{urllib.parse.quote(key)}?" + \
        urllib.parse.urlencode(query)
    req = urllib.request.Request(url, headers={
        "Authorization": auth_header,
        "Accept": "application/json",
        "User-Agent": "jira-fetch-skill/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        raise SystemExit(
            f"ERROR: Jira returned HTTP {exc.code} for {key}.\n"
            f"  URL: https://{domain}/rest/api/{version}/issue/{key}\n"
            f"  Hint: 401/403 = bad token/permissions; 404 = wrong key or domain.\n"
            f"  Body: {body}"
        )
    except urllib.error.URLError as exc:
        raise SystemExit(f"ERROR: could not reach https://{domain} — {exc.reason}")

    comments = None
    if with_comments:
        curl = f"https://{domain}/rest/api/{version}/issue/{urllib.parse.quote(key)}/comment"
        creq = urllib.request.Request(curl, headers={
            "Authorization": auth_header, "Accept": "application/json",
            "User-Agent": "jira-fetch-skill/1.0",
        })
        try:
            with urllib.request.urlopen(creq, timeout=30) as resp:
                comments = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError:
            comments = None
    return data, comments


def human_size(num):
    """Render a byte count as a compact human string (e.g. 12.3 KB)."""
    try:
        num = float(num)
    except (TypeError, ValueError):
        return "?"
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} GB"


def safe_filename(name, fallback):
    """Strip path separators / unsafe chars so an attachment name can't escape DIR."""
    name = os.path.basename(name or "").strip() or fallback
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)


def download_attachments(attachments, dest_dir, auth_header):
    """Download each attachment's binary into dest_dir. Returns list of result dicts.

    Uses the attachment's authenticated `content` URL. Never overwrites blindly:
    duplicate names get an id suffix so nothing is clobbered.
    """
    os.makedirs(dest_dir, exist_ok=True)
    results = []
    used = set()
    for att in attachments or []:
        content_url = att.get("content")
        att_id = str(att.get("id", ""))
        if not content_url:
            results.append({"filename": att.get("filename"), "error": "no content URL"})
            continue
        fname = safe_filename(att.get("filename"), f"attachment-{att_id}")
        if fname in used:  # de-dupe on identical names within one issue
            stem, ext = os.path.splitext(fname)
            fname = f"{stem}-{att_id}{ext}"
        used.add(fname)
        target = os.path.join(dest_dir, fname)
        req = urllib.request.Request(content_url, headers={
            "Authorization": auth_header,
            "User-Agent": "jira-fetch-skill/1.0",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as resp, open(target, "wb") as fh:
                fh.write(resp.read())
            results.append({
                "filename": fname, "path": target,
                "mimeType": att.get("mimeType"), "size": att.get("size"),
            })
        except (urllib.error.URLError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            results.append({"filename": fname, "error": str(reason)})
    return results


def adf_to_text(node, depth=0):
    """Flatten Atlassian Document Format (v3 description) into plain text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    parts = []
    ntype = node.get("type")
    if ntype == "text":
        return node.get("text", "")
    if ntype == "hardBreak":
        return "\n"
    if ntype in ("paragraph", "heading"):
        inner = "".join(adf_to_text(c, depth) for c in node.get("content", []))
        return inner + "\n"
    if ntype in ("bulletList", "orderedList"):
        for i, item in enumerate(node.get("content", []), 1):
            bullet = "- " if ntype == "bulletList" else f"{i}. "
            parts.append("  " * depth + bullet + adf_to_text(item, depth + 1).strip())
        return "\n".join(parts) + "\n"
    if ntype == "listItem":
        return "".join(adf_to_text(c, depth) for c in node.get("content", []))
    if ntype == "codeBlock":
        inner = "".join(adf_to_text(c, depth) for c in node.get("content", []))
        return f"```\n{inner}\n```\n"
    for child in node.get("content", []):
        parts.append(adf_to_text(child, depth))
    return "".join(parts)


def describe(data, comments, downloaded=None):
    fields = data.get("fields", {})

    def name_of(obj, key="displayName"):
        if isinstance(obj, dict):
            return obj.get(key) or obj.get("name") or obj.get("value") or ""
        return obj or ""

    desc_field = fields.get("description")
    if isinstance(desc_field, dict):       # ADF (API v3)
        description = adf_to_text(desc_field).strip()
    elif desc_field:                        # plain text/wiki (API v2)
        description = str(desc_field).strip()
    else:
        description = ""

    lines = []
    lines.append(f"# {data.get('key', '?')}: {fields.get('summary', '')}")
    lines.append("")
    lines.append(f"- Type:      {name_of(fields.get('issuetype'), 'name')}")
    lines.append(f"- Status:    {name_of(fields.get('status'), 'name')}")
    lines.append(f"- Priority:  {name_of(fields.get('priority'), 'name')}")
    lines.append(f"- Assignee:  {name_of(fields.get('assignee')) or 'Unassigned'}")
    lines.append(f"- Reporter:  {name_of(fields.get('reporter'))}")
    if fields.get("parent"):
        p = fields["parent"]
        lines.append(f"- Parent:    {p.get('key', '')} {p.get('fields', {}).get('summary', '')}")
    if fields.get("labels"):
        lines.append(f"- Labels:    {', '.join(fields['labels'])}")
    comps = [name_of(c, 'name') for c in fields.get("components", []) or []]
    if comps:
        lines.append(f"- Component: {', '.join(comps)}")
    fixv = [name_of(v, 'name') for v in fields.get("fixVersions", []) or []]
    if fixv:
        lines.append(f"- Fix ver:   {', '.join(fixv)}")
    if name_of(fields.get("resolution"), "name"):
        lines.append(f"- Resolved:  {name_of(fields.get('resolution'), 'name')}")
    lines.append(f"- Created:   {fields.get('created', '')}")
    lines.append(f"- Updated:   {fields.get('updated', '')}")
    lines.append("")
    lines.append("## Description")
    lines.append(description if description else "_(empty)_")

    attachments = fields.get("attachment") or []
    if attachments:
        dl_by_name = {r.get("filename"): r for r in (downloaded or [])}
        lines.append("")
        lines.append(f"## Attachments ({len(attachments)})")
        for att in attachments:
            fname = att.get("filename", "?")
            meta = f"{human_size(att.get('size'))}, {att.get('mimeType', '?')}"
            author = name_of(att.get("author"))
            created = att.get("created", "")
            entry = f"- **{fname}** ({meta})"
            if author or created:
                entry += f" — {author} {created}".rstrip()
            saved = dl_by_name.get(safe_filename(fname, ""))
            if saved and saved.get("path"):
                entry += f"\n  - saved to: `{saved['path']}`"
            elif saved and saved.get("error"):
                entry += f"\n  - download failed: {saved['error']}"
            lines.append(entry)
        if downloaded:
            lines.append("")
            lines.append(
                "_Open the saved image/PDF/log attachments above to analyse the "
                "reported problem alongside the Description._"
            )

    if comments and comments.get("comments"):
        lines.append("")
        lines.append(f"## Comments ({comments.get('total', len(comments['comments']))})")
        for c in comments["comments"]:
            author = name_of(c.get("author"))
            body = c.get("body")
            text = adf_to_text(body).strip() if isinstance(body, dict) else str(body or "").strip()
            lines.append(f"\n**{author}** ({c.get('created', '')}):")
            lines.append(text)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch a Jira issue by key or URL.")
    parser.add_argument("issue", help="Issue key (PROJ-123) or a Jira URL")
    parser.add_argument("--comments", action="store_true", help="Include comments")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of summary")
    parser.add_argument("--env", help="Path to .claude/.env (auto-detected if omitted)")
    parser.add_argument(
        "--download-attachments", nargs="?", const="__DEFAULT__", metavar="DIR",
        dest="download_attachments",
        help="Download the issue's attachments into DIR "
             "(default: ./jira-attachments/<KEY>/) so they can be opened/analysed.",
    )
    args = parser.parse_args()

    env_path = find_env_file(args.env)
    env = load_env(env_path)

    key = extract_issue_key(args.issue)
    if not key:
        raise SystemExit(
            f"ERROR: could not find an issue key (e.g. PROJ-123) in: {args.issue!r}"
        )

    # A full URL in the input overrides JIRA_DOMAIN; otherwise require config.
    domain = domain_from_input(args.issue) or (env.get("JIRA_DOMAIN") or "").strip()
    if not domain:
        raise SystemExit(
            f"ERROR: JIRA_DOMAIN not set in {env_path} and no domain in the input URL."
        )
    domain = domain.replace("https://", "").replace("http://", "").rstrip("/")

    version = (env.get("JIRA_API_VERSION") or "3").strip()
    auth_header = build_auth_header(env)

    data, comments = fetch_issue(domain, version, key, auth_header, args.comments)

    downloaded = None
    if args.download_attachments is not None:
        attachments = (data.get("fields") or {}).get("attachment") or []
        if attachments:
            dest = args.download_attachments
            if dest == "__DEFAULT__":
                dest = os.path.join("jira-attachments", data.get("key", key))
            downloaded = download_attachments(attachments, dest, auth_header)

    if args.raw:
        out = {"issue": data}
        if comments is not None:
            out["comments"] = comments
        if downloaded is not None:
            out["downloaded_attachments"] = downloaded
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(describe(data, comments, downloaded))
        print(f"\n---\nLink: https://{domain}/browse/{data.get('key', key)}")


if __name__ == "__main__":
    main()
