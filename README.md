# Orchestrate Codex Super Save

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An opt-in, Luna-only Codex orchestration profile designed to minimize delegation,
context duplication, and coordination overhead. It uses your existing Codex sign-in
and native subagents. No API key or external model service is required.

## Worker profile

| Worker | Model | Effort |
|---|---|---|
| Scout | GPT-5.6 Luna | medium |
| Researcher | GPT-5.6 Luna | xhigh |
| Coder | GPT-5.6 Luna | max |
| Architect | Session model | Explicit approval before every launch |

The main agent handles small or serial work directly. At most two children run at
once. Architect escalation happens only after an ordinary attempt plus a focused
diagnostic pass fail to resolve the problem.

## Install

Review the installer, then run:

```text
python scripts/install.py
```

This installs a separate `$orchestrate-super-save` skill and four uniquely named
`super-save-*` role profiles. It does not change your default Orchestrate skill or
global routing instructions. Restart Codex after installation.

Example:

```text
$orchestrate-super-save Compare these two SDKs, implement the selected adapter, and verify it.
```

## Validate

```text
python scripts/validate.py
python scripts/test_install.py
```

The checks validate the package and isolated installation behavior. They do not prove
that a particular account currently exposes every listed model and effort combination.

Licensed under the [MIT License](LICENSE).

