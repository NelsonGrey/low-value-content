# Security Policy

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Report privately using GitHub's **Report a vulnerability** option on the repository's Security tab (private vulnerability reporting), or contact the repository owner, [@mnelson3](https://github.com/mnelson3), directly.

Include what you found, how to reproduce it, and the potential impact. You can expect an acknowledgement within a few business days.

## Scope

- The Low Value Content website (`website/dist/` and its Firebase Hosting deployments)
- GitHub Actions workflows and deployment configuration
- Accidentally exposed secrets or personal data in the repository

## Handling secrets

If you find a committed credential, report it privately. Do not use it. It will be rotated and removed from history if needed.
