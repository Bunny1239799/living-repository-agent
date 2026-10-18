# Evidence Synthesis

Mission: `002-research-engine`
Question: Which GitHub Actions controls should LRA review to reduce workflow security risks and preserve least privilege?

## Evidence grouped for review

The groups below contain source-linked excerpts, not autonomous or independently verified conclusions.

### Token permissions and least privilege
- Learn what GITHUB_TOKEN is, how it works, and why it matters for secure automation in GitHub Actions workflows. [S1]
- At the start of each workflow job, GitHub automatically creates a unique GITHUB_TOKEN secret to use in your workflow. [S1]
- You can use the GITHUB_TOKEN to authenticate in the workflow job. [S1]
- The GITHUB_TOKEN secret is a GitHub App installation access token. [S1]
- The token's permissions are limited to the repository that contains your workflow. [S1]
- Therefore, you should ensure that the credentials being used within workflows have the least privileges required. [S2]

### Untrusted input and script injection
- Understand the security risks associated with script injections and GitHub Actions workflows. [S3]
- When creating workflows, custom actions, and composite actions, you should always consider whether your code might execute untrusted input from attackers. [S3]
- Attackers can add their own malicious content to the github context, which should be treated as potentially untrusted input. [S3]
- For example: github.event.issue.title, or github.event.pull_request.body. [S3]
- In addition, there are other less obvious sources of potentially untrusted input, such as branch names and email addresses, which can be quite flexible in terms of their permitted content. [S3]

## Conclusions and unknowns
- This output is an extractive evidence digest, not a verified security audit.
- Repository-specific security cannot be inferred from documentation alone.
- Review workflow permissions, action pinning, event trust boundaries, and runtime tests before drawing implementation conclusions.
- Human review remains required; this engine does not approve or stage changes.

## Sources
- [S1] GITHUB_TOKEN - GitHub Docs: https://docs.github.com/en/actions/concepts/security/github_token
- [S2] Secure use reference - GitHub Docs: https://docs.github.com/en/actions/reference/security/secure-use
- [S3] Script injections - GitHub Docs: https://docs.github.com/en/actions/concepts/security/script-injections