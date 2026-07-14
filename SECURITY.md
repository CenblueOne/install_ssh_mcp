# Security Policy

## Scope
This MCP server grants shell access to a remote host via SSH. Treat it like
direct server credentials.

## Reporting a Vulnerability
If you find a security issue, **do not open a public issue**. Contact the
maintainer privately via GitHub Security Advisories or a direct message.

## Safe Usage
- **Never commit** `.env` or private keys (`*.pem`, `*.key`). They are
  git-ignored on purpose.
- Only point `VPS_HOST` / `VPS_USER` / `VPS_KEY_PATH` at servers you own or
  are explicitly authorized to control.
- Restrict the SSH key on the target host to the minimum commands needed.
- Rotate keys immediately if they are ever exposed.

## Secrets Handling
- `.env` holds live credentials — keep it local only.
- `.env.example` is safe to commit (no real values).
- If a secret was accidentally pushed, rotate it and purge history
  (`git filter-repo` / GitHub "Remove sensitive data").
