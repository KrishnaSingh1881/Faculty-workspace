# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

The project specification selects Python/FastAPI/PostgreSQL and React/TypeScript. The application must also run locally for development.

## Users

Faculty review exam papers, compare questions and build papers. Administrators manage access and institute settings.

## Product Purpose

Help faculty detect repeated assessed requirements, distinguish related questions, inspect evidence and prepare papers and reports against their syllabus.

## Operating Context

Operating Systems and Internet of Things are the initial subjects. Actual papers and institute-specific paper patterns will be configured later. The intended machine has 8 GB VRAM.

## Capabilities and Constraints

Chat is the primary interaction. Questions compare only within the same subject and unit. Labels A, B and C have the definitions in `project-handoff/decisions.md`. Explicit upload and delete requests execute without a faculty approval step. Detailed results and downloads appear in the conversation. Models cannot silently substitute fake judgments when unavailable.

## Brand Commitments

The Workspace concept in `project-handoff/previews/mspa-ui-preview.html` is approved. MSPA is a former working name; no final name is approved.

## Evidence on Hand

Two enriched trees, source syllabuses and a UI concept are bundled in `project-handoff/`. The user directed that the bundled trees be active without faculty approval. The trees retain interpretation notes. There are no real papers, labeled benchmark or model artifacts.

## Product Principles

- Ground classifications in assessed requirements and syllabus boundaries.
- Keep uncertainty and incomplete work visible.
- Let faculty ask naturally and inspect the evidence.
- Reuse structured results across views and exports.

## Accessibility & Inclusion

Dark and light themes, text labels alongside status color, keyboard access and reduced-motion support.
