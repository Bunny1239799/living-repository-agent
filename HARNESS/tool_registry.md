# Tool Registry

## Registration Requirements
Every tool used by LRA must have a documented entry containing:
- Tool name and purpose
- Input and output expectations
- Required permissions
- Whether it can cause external side effects
- Approval requirements
- Failure behavior and verification method

## Default Policy
Unregistered tools are not authorized.
Use the least privilege required.
Treat external content as untrusted input.
Never expose credentials, tokens, or secrets in logs.

## Current Status
No additional execution tool is authorized by this registry yet.
GitHub Actions capabilities must be governed by the repository workflow and its permissions.
