# Project handoff - exam question redundancy assistant

This is the source-specification and review bundle used by the implemented workspace in the parent project. The final product name has not been chosen. MSPA is the former working name.

## Start here

1. Read `decisions.md` for accepted direction and unresolved choices.
2. Read `original-spec.md` alongside the decisions; the original spec has not been rewritten to incorporate the conversation.
3. Review `trees/tree-review-guide.md` and the two readable tree reviews.
4. Use `chat-transcript.md` for conversation context. It preserves user/assistant text, not tool activity or hidden reasoning.
5. Treat the transcript as historical context and `decisions.md` as the current accepted direction. The application source is in the parent project; this bundle contains its specification, trees, review notes and source documents.

## Contents

- `trees/`: proposed enriched JSON trees, readable reviews and structural validation.
- `sources/`: original syllabus PDFs and original model-populated tree attachments.
- `previews/`: HTML fragments for the UI and full tree explorer. These depend on the conversation visualization host for styling and some behavior; they are not standalone applications. Their source is preserved for rebuilding the design.
- `original-spec.md`: the complete initial specification.
- `chat-transcript.md`: conversation export through the packaging request.
- `decisions.md`: concise continuation context.
- `manifest.json`: SHA-256 checksums for verifying transfer.

## Continue on Linux or WSL2

Copy this folder or its ZIP archive to the target environment. Extract it to a project directory in the Linux home filesystem, for example `~/projects/exam-assistant-planning`. Open that folder in your coding agent and ask it to read this README, decisions, original spec and tree reviews before proposing changes.

Windows absolute paths inside the transcript are historical references. Use the files inside this bundle instead. The JSON trees retain their original provenance paths, but the input copies are available under `sources/`.

Copying this Markdown transcript does not import a native chat into another client. It supplies portable context to a new chat. Do not copy account tokens or credentials as part of migration.

## Status and assumptions

- The supplied OS and IoT trees are accepted for use without a faculty-approval step. Interpretation notes are informational.
- OS and IoT are the initial subjects; adding other subjects can use the syllabus import workflow.
- 8 GB VRAM is known; exact GPU, system RAM, OS distribution and runtime compatibility remain unverified.
- The parent project contains a working application implementation in progress. No labeled benchmark result or final dependency lockfile exists yet.
- The project is one full agreed product build, with internal checkpoints, not a sequence of reduced product releases.
- This README describes the source bundle and continuation context. Follow the latest decisions in `decisions.md` where old transcript or original-spec language conflicts.
