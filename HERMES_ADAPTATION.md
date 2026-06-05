# Hermes Agent adaptation notes

This branch adapts `fivetaku/insane-search` for Hermes Agent usage while preserving the original MIT-licensed project structure.

Original project: https://github.com/fivetaku/insane-search
Fork: https://github.com/0yeonnnn0/insane-search
Working branch: `hermes-adaptation`

## Goal

Use insane-search as a reusable **blocked web access fallback** skill for Hermes Agent:

1. Prefer official/public APIs and RSS/Atom endpoints when available.
2. Use lightweight readers such as Jina Reader for ordinary articles.
3. Try mobile URL transforms and TLS impersonation for public pages that block default fetchers.
4. Use Hermes browser tools to inspect rendered pages and network requests when HTML is blocked but a public JSON API may exist.
5. Stop at authentication, payment, CAPTCHA, or explicit permission boundaries.

## What changed first

- Added `engine/deps.py` for contained runtime dependency bootstrap.
- Made the documented “auto dependency install” behavior real for:
  - `curl_cffi`
  - `beautifulsoup4`
  - `PyYAML`
- Added `skills/insane-search/requirements.txt` for explicit pre-install.

Runtime installs can be disabled with:

```bash
INSANE_SEARCH_NO_AUTO_INSTALL=1 python3 -m engine "https://example.com/"
```

Recommended explicit install:

```bash
python3 -m pip install --user -r skills/insane-search/requirements.txt
```

## Hermes tool mapping

The upstream skill mentions Claude/MCP tool names such as `mcp__playwright__browser_navigate`. In Hermes sessions, use these equivalents:

| Upstream concept | Hermes equivalent |
|---|---|
| browser navigate | `browser_navigate` |
| snapshot/DOM read | `browser_snapshot` |
| page evaluate / network inspection | `browser_console(expression=...)` |
| screenshots/visual checks | `browser_vision` |
| shell CLI execution | `terminal` |
| file inspection | `read_file`, `search_files` |
| targeted edits | `patch` |

## Safety boundary

This adaptation is for public web access troubleshooting and fallback discovery. Do not use it to bypass login, paywalls, CAPTCHA, rate limits, or access controls. When a page requires authentication or user permission, stop and ask the user to provide a legitimate session/context or use an official API.

## Next adaptation tasks

- Rewrite `SKILL.md` trigger/rules in Hermes-native language.
- Replace Claude MCP examples with Hermes browser tool recipes.
- Add a small smoke test script that verifies dependency bootstrap and `example.com` fetch.
- Add Korean web references for Naver Blog/News, shopping pages, and public community pages.
