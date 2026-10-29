# Full implementation plan

This is one complete web-app build. It starts from the existing FastAPI and React source; it is not a demo milestone. [progress.md](progress.md) records what already exists, and [remaining-tasks.md](remaining-tasks.md) is the detailed gap inventory. This plan groups that work into the smallest set of complete delivery tasks.

## Governing decisions

- The approved chat-first Workspace design is the product UI. The bundled OS and IoT enriched trees are active, with their interpretation notes visible.
- Uploads and explicit edits or deletions take effect on request. There is no faculty approval, second confirmation, or deletion gate. Uncertain extraction and model results remain visible and directly correctable.
- A means equivalent assessed requirements; B means meaningful overlap with differences; C means no meaningful assessed overlap. Comparison is within the same subject and unit. An unresolved result is allowed when the evidence is inadequate.
- The finished application must work before actual college paper patterns, department report templates, or a labeled real-paper corpus are supplied. Those inputs must be configurable later through the app without code changes. Default schemas and layouts are part of this build; invented institute patterns are not.
- Model inference is local to the machine or private host running the app. Do not send question, syllabus or paper content to OpenAI, Anthropic or other external model APIs. The 8 GB VRAM limit shapes local model choice and scheduling; final model choice and accuracy claims require representative material and measurements.

## Build order and completion criteria

| Order | Delivery task | Complete when |
| --- | --- | --- |
| 1 | **Stabilize the existing source and dependencies.** Fix the current API import/startup defect and any failures exposed by clean API import, tests and frontend build. Remove old approval paths. Pin Python and Node dependencies; keep one shared implementation for chat and manual actions. | A fresh checkout can install, migrate, start the API and UI, sign in, and pass the existing checks. The current code has been verified after its latest edits. |
| 2 | **Make storage and background work durable.** Add PostgreSQL/pgvector migrations, constraints, indexes, file hashing, revisions, audit records, backup/restore, and a restart-safe job queue. Run local inference with a supported local model runtime; coordinate OCR, embeddings and LLM work through bounded batches and a single GPU scheduler. Keep local and shared-host account/subject isolation. | An upload or comparison survives process restart, resumes or reports failure accurately, and preserves its sources, versions and audit history. A teacher cannot access another teacher's restricted data. Model requests remain within the machine or private host. |
| 3 | **Finish syllabus onboarding and tree management.** Import syllabus PDF/Office/text/image into a validated five-unit subject tree; preserve official wording, IDs and hierarchy. Add direct corrections, JSON import/export, topic-link edits, history, diff, restore and targeted re-enrichment. Make OS and IoT active from the bundled trees. | A new subject can be onboarded from a syllabus through the UI/chat, edited and restored; invalid structure is rejected without silently inventing nodes. |
| 4 | **Finish paper and teaching-resource ingestion.** Store originals; process typed/scanned documents in resumable page batches; extract questions, subparts, OR/choose-any choices, marks and metadata; permit direct fixes. Map whole teaching resources to relevant topics, create cited enrichment, detect conflicting or out-of-syllabus claims, validate and apply safe patches. Add bulk import, duplicates, revisions, archive/restore, search and immediate deletion with dependent-result invalidation. | A long resource and a paper can be uploaded end to end, with page/slide citations, progress, uncertain passages, editable mappings, valid marks and no dangling results after a delete. |
| 5 | **Build the local assessment engine and actual helper tools.** Extract and cache atomic requirements; retrieve candidate pairs with a high-recall escape beyond topic tags; give a helper model an independent, blinded comparison; let the judge model call evidence and alignment tools before deciding; enforce deterministic invariants and abstention. Store evidence spans, tool inputs/outputs, disagreements, versions and unresolved outcomes; cache by question and decision configuration. | Same-subject/same-unit pairs receive defensible A/B/C or unresolved results. A shared subpart alone cannot make a compound pair A; adjacency alone cannot make B; weak topic tags cannot silently exclude a strong candidate. Changes mark affected results stale. No question content leaves the machine/private host. |
| 6 | **Complete comparisons, templates and reports.** Save reusable comparison scopes and exact target/reference rules. Implement separate paper-pattern, question-slot and report-template schemas with defaults; accept later chat descriptions or uploaded templates, field mapping, editing, preview and versioning. Render structured results to MD, TXT, PDF and XLSX without rerunning the classifier. | Faculty can configure an actual pattern or report layout later, preview it, use it immediately, and re-export an existing result. Incomplete/stale classifications stay visible in every format. |
| 7 | **Complete the chat-first Workspace.** Replace the finite command router with grounded tool use for onboarding, upload, editing, comparing, evidence inspection, templates, export, generation and explicit deletion. Resolve context from the conversation and offer inline choices when details are genuinely missing. Persist messages, actions, file cards, job events and downloads. Finish corpus, comparison, graph, analytics, bank, generation, draft, skills/rules and report surfaces in the approved design, including responsive and accessible light/dark UI. | A faculty member can carry out every primary workflow from chat, reopen it later, inspect real tool/evidence events and use the corresponding Workspace views. Explicit actions execute directly. |
| 8 | **Deliver paper analysis and search.** Compute paper health, predictability, level/difficulty, marks balance, choice fairness, subpart overlap, answer-leak indicators, unit/year coverage, trends and syllabus graph from documented formulas and chosen reference scopes. Provide searchable, filtered question bank. | Each metric is reproducible from stored questions and scope, exposes its inputs, and handles insufficient evidence without a fabricated authoritative score. |
| 9 | **Deliver replacement and draft building.** Generate slot blueprints from configured paper patterns, unit/marks/level targets and coverage gaps; suggest replacements; edit/regenerate questions; check each candidate against selected past papers and the current draft with the same assessment engine. Show cheap checks immediately and model checks as pending until complete. | A draft can be built, revised, checked, saved and exported. A generated question is never labeled novel until its redundancy check passes; generated material stays out of evaluation data. |
| 10 | **Package and verify the finished application.** Provide Docker Compose and a documented non-Docker path, health checks, operational settings, HTTPS/shared-host guidance, structured logs, typed API contract and release documentation. Add focused migration, security, restart-recovery, backend and browser workflow checks, then run a clean-install/full-stack smoke test. Keep the benchmark runner able to accept later labeled OS/IoT cases and compare engine variants. | A new installation can complete the end-to-end workflow below, survives a restart, enforces access rules and exports usable files. Failures are reported rather than replaced by fake model judgments. |

## End-to-end delivery check

From a fresh install: open the Workspace; use an active OS/IoT tree or upload another syllabus; upload teaching material and see cited enrichment across its relevant pages; upload and correct a paper; compare it against selected references; inspect A/B/C or unresolved evidence and helper trace; view health, coverage and bank results; generate or replace a question and build a draft; configure a paper pattern and a report layout; export all supported formats; delete a selected item directly; restart the stack and find the conversation, files, jobs and unaffected results intact. This check uses generated fixtures and default layouts because real institute samples are not available yet.

## Classifier design in detail

The classifier is a local module with one small interface: given two versioned questions, their confirmed unit/topic tags, the active syllabus tree, and a versioned decision configuration, return a validated `A`, `B`, `C`, or `review` result with evidence and a complete trace. It owns the order of analysis, retrieval, tool calls, judge/helper coordination, validation, caching and abstention. Chat and batch comparisons call the same interface.

### 1. Build grounded question records

For each question, a local analysis model produces a structured requirement record, tied to exact text spans:

- atomic asks and their subpart/OR/choose-any structure;
- concept or method, action verb, object, scope and expected output;
- depth/operation, constraints, conditions, negation and qualifiers;
- formula or numerical procedure when the text states one;
- likely syllabus topic IDs, with confidence and an explicit unknown option.

The record is evidence-linked, not accepted as truth by itself. Faculty edits update the question revision and invalidate downstream records. Retrieval and comparison retain the original text so a bad parse cannot hide a relevant match.

### 2. Retrieve candidates for recall

Only compare within the same subject and unit, but use multiple candidate paths: confirmed topic tags and tree aliases; lexical overlap; CPU-friendly semantic vectors; and requirement/action/object signals. Take the union of candidates, then rank it for processing. Topic mismatch alone never removes a candidate. Measure candidate recall on labeled held-out question families before setting any pruning threshold; when confidence is low, widen the candidate set rather than silently skip pairs.

### 3. Let the helper investigate independently

The local helper model receives both original questions, their requirement records and the applicable syllabus evidence, but not the judge's proposed label or rationale. It returns a requirement-by-requirement alignment table with source spans, exact/partial/no match, extra asks, contradictions, compound-part mapping, and the strongest counterexample to equivalence. It cannot write syllabus facts or assign the final A/B/C label.

The helper can call typed tools implemented by the application:

- **Syllabus lookup:** return exact node, ancestor path, definition, boundary, aliases, same-unit distinction notes and citations.
- **Requirement comparison:** align two atomic asks and report shared, narrower, broader, missing, additional or contradictory requirements with text spans.
- **Compound alignment:** find the best one-to-one mapping, report unmatched parts, preserve OR/choice rules, and evaluate coverage in both directions.
- **Transformation check:** test whether wording/scenario changes preserve the demanded operation, scope, output and depth; return which dimension changed.
- **Evidence search:** retrieve supporting or disconfirming text from the questions and syllabus. It may return “no evidence”; it cannot manufacture support.

These are real application functions with validated inputs and structured outputs, not instructions to imagine using tools. Every call and result is stored in the trace.

### 4. Make and challenge the judgment

The local judge sees the questions, requirement records, helper alignment, cited syllabus records and tool outputs. It must decide from assessed requirements, not shared vocabulary, topic adjacency, marks or the helper's conclusion. A bounded challenge pass asks what would make the proposed label wrong and checks missed/extra compound asks. A distinct local helper model is required for independent review. Due to 8 GB VRAM, judge and helper models run sequentially and are unloaded between jobs as needed; the model pair must be selected and measured to fit this schedule.

Label rules:

- **A:** assessed requirements match in concept, task, scope and expected depth in both directions; all required compound parts align.
- **B:** there is material assessed overlap, but at least one requirement, scope, depth, condition or compound part differs or is additional.
- **C:** the supplied evidence supports no meaningful assessed overlap. Missing tags, absent retrieved evidence or unfamiliar wording alone are insufficient for C.
- **review:** extraction, retrieval, evidence or model outputs conflict or are too weak to support a label.

### 5. Verify, calibrate and retain the trace

Deterministic code checks subject/unit scope, valid topic IDs, evidence spans, full compound coverage for A, both-direction requirement coverage, output schema, model/tool completion and cache versions. It rejects invalid results and converts unresolved conflicts to `review`; it does not pretend to prove semantic truth with rules. Calibrate confidence and any automatic abstention threshold against a held-out, family-separated labeled corpus. Store question snapshots, requirement records, candidate-retrieval reasons, helper alignment, every tool call, judge/challenge outputs, cited spans, model identifiers/quantization, prompt/tool/rule versions, decision and uncertainty. Cache keys include question revisions, syllabus version and all decision/model/tool configuration; edits make affected results stale.

### 6. Prove the classifier before calling it robust

Build a labeled OS/IoT set with distinct question families in development and held-out partitions. Include equivalent rewordings; same-topic different-task pairs; sibling topics; differing depth/scope; negation and conditions; numerical methods; partial and whole-question overlap; OR/choice structures; incomplete or wrong tags; and extraction noise. Measure candidate recall, per-label precision/recall, confusion matrix, compound alignment, evidence correctness, abstention rate, repeatability, latency and GPU memory. Compare judge-only, helper-enabled, tool-enabled and retrieval variants. Fix release thresholds before evaluating the held-out set. Until that measurement passes, the product may return provisional/review results but must not advertise the classifier as robust.

## Inputs and work after the build

Actual paper patterns, report templates, sample papers and scanned/handwritten resources are configuration and validation inputs **after** the application is built. The app must already provide the import, mapping, correction and rendering flows for them. Real OS/IoT labeling, OCR correction-effort measurement, final local model selection on the 8 GB GPU, score calibration and faculty acceptance testing follow when those inputs are available. Until measured, report engineering checks as passing or failing, but do not claim classification or handwriting accuracy.

Faculty-feedback propagation, precedent learning, automatic model training and a desktop wrapper remain later features. Case-specific corrections and their audit trail belong in this build.
