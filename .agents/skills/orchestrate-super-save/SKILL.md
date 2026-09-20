---
name: orchestrate-super-save
description: Use when the user explicitly requests Orchestrate Super Save, ultra-conservative delegation, or the configured Luna-only worker fleet.
---

# Orchestrate Super Save

Optimize for low coordination and context overhead, not for the fewest reasoning
tokens inside every worker. The main agent owns scope, sequencing, integration, and
verification. Preserve an explicitly selected user model and all permission limits.

## Workers

| Role | Model / effort | Use |
|---|---|---|
| scout | gpt-5.6-luna / medium | Narrow code or file inspection |
| researcher | gpt-5.6-luna / xhigh | One difficult research or diagnosis question |
| coder | gpt-5.6-luna / max | One scoped implementation with checks |
| architect | parent session model / effort | Approved escalation only |

Use the matching `super-save-*` custom agent when available. Otherwise use native
spawning with the listed model and effort. If routing is unavailable, work serially
and disclose that limitation.

## Routing rules

1. Keep trivial, known, or serial work with the main agent. Do not spawn a worker
   merely to rename text, read one known file, or apply an obvious local fix.
2. Delegate only a bounded unit that benefits from isolated context. Give the worker
   its outcome, allowed paths, constraints, and required evidence.
3. Run at most two children concurrently. If three or more independent units exist,
   queue them in waves of two and reuse a completed worker of the same role for related
   follow-up when the host supports it.
4. Do not duplicate investigation between parent and child. Read narrow paths, keep
   prompts short, and request concise results.
5. Use researcher for source-backed comparison or deeper diagnosis. Use coder only
   after dependencies and ownership are clear. Editing workers must have disjoint files.
6. A failed coder attempt does not automatically justify architect. First correct
   missing context, reproduce the failure, or run one focused scout/researcher pass.
7. Launch architect only for a still-unresolved hard problem and only after explicit
   user approval immediately before that launch. Approval does not carry to retries.
8. Collect every delegated result, inspect changed files, and run final verification.
   Worker completion alone is not proof.

Stop when the requested outcome and proportionate verification are complete. Report
the outcome, evidence, checks, blockers, and next action without inventing extra stages.
