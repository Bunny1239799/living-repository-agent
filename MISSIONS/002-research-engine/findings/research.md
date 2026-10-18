# Research Findings

Mission: `002-research-engine`
Research question: Which GitHub Actions controls should LRA review to reduce workflow security risks and preserve least privilege?
Retrieved at (UTC): 2026-10-18T16:25:29.648419+00:00

Method: bounded HTTPS retrieval from configured allowlisted hosts; keyword-matched extractive evidence. Source text is untrusted input.

## Source-linked evidence

### [S1] GITHUB_TOKEN - GitHub Docs
- Configured URL: https://docs.github.com/en/actions/concepts/security/github_token
- Final URL: https://docs.github.com/en/actions/concepts/security/github_token
- HTTP status: 200
- Retrieved at: 2026-10-18T16:25:26.850872+00:00

- Evidence excerpt: Learn what GITHUB_TOKEN is, how it works, and why it matters for secure automation in GitHub Actions workflows. [S1]
- Evidence excerpt: At the start of each workflow job, GitHub automatically creates a unique GITHUB_TOKEN secret to use in your workflow. [S1]
- Evidence excerpt: You can use the GITHUB_TOKEN to authenticate in the workflow job. [S1]
- Evidence excerpt: The GITHUB_TOKEN secret is a GitHub App installation access token. [S1]
- Evidence excerpt: The token's permissions are limited to the repository that contains your workflow. [S1]

### [S2] Secure use reference - GitHub Docs
- Configured URL: https://docs.github.com/en/actions/reference/security/secure-use
- Final URL: https://docs.github.com/en/actions/reference/security/secure-use
- HTTP status: 200
- Retrieved at: 2026-10-18T16:25:28.593062+00:00

- Evidence excerpt: Adhere to the following best practices to limit risks associated with secrets. [S2]
- Evidence excerpt: Any user with write access to your repository has read access to all secrets configured in your repository. [S2]
- Evidence excerpt: Therefore, you should ensure that the credentials being used within workflows have the least privileges required. [S2]
- Evidence excerpt: Redacting of secrets is performed by your workflow runners. [S2]
- Evidence excerpt: For example, do not use a blob of JSON, XML, or YAML (or similar) to encapsulate a secret value, as this significantly reduces the probability the secrets will be properly redacted. [S2]

### [S3] Script injections - GitHub Docs
- Configured URL: https://docs.github.com/en/actions/concepts/security/script-injections
- Final URL: https://docs.github.com/en/actions/concepts/security/script-injections
- HTTP status: 200
- Retrieved at: 2026-10-18T16:25:29.647685+00:00

- Evidence excerpt: Understand the security risks associated with script injections and GitHub Actions workflows. [S3]
- Evidence excerpt: When creating workflows, custom actions, and composite actions, you should always consider whether your code might execute untrusted input from attackers. [S3]
- Evidence excerpt: Attackers can add their own malicious content to the github context, which should be treated as potentially untrusted input. [S3]
- Evidence excerpt: For example: github.event.issue.title, or github.event.pull_request.body. [S3]
- Evidence excerpt: In addition, there are other less obvious sources of potentially untrusted input, such as branch names and email addresses, which can be quite flexible in terms of their permitted content. [S3]

## Limitations
- Extracted excerpts are not independently fact-checked.
- Retrieval proves the page was accessible, not that every claim is true.
- No model-generated factual claims were added.
