# Accepted direction and open decisions

## Product

- Build a local/shared-host web application for syllabus-aware exam-question redundancy and paper analysis. Desktop packaging is optional later. Product rename requested; no name selected.
- Primary interface resembles GPT/Claude: faculty asks in chat; inline choices resolve missing information; results, evidence, previews and downloadable files appear in conversation.
- Workspace UI concept was approved. Permanent buttons for every action are not the intended experience. Sidebar supports navigation; evidence panels open when useful.
- Uploaded content is final when submitted. Explicit deletion requests are final and execute directly. No faculty-approval or deletion-confirmation workflow is required.
- Dark/light themes, system default, persistent preference, accessible classification labels and reduced-motion support are required.

## Classification

- A: equivalent assessed concept, task, scope and expected depth. B: meaningful assessed overlap with differences/additions. C: no meaningful assessed overlap.
- One matching compound part does not make the entire pair A.
- Subject has five units, with topics/subtopics; each exam question belongs to exactly one unit. Compare selected base-paper questions with selected references in the same subject and unit only.
- Syllabus adjacency cannot decide B. No topic overlap/adjacency is not sufficient proof of C; candidate exclusion needs a strong-match/uncertain-tag escape route.
- Cache pair judgments using question revisions and the decision configuration, not pair ID alone.
- Classification robustness is the priority. Syllabus tools, question-requirement analysis, judge/helper and deterministic validation perform the work; explanations can be detailed and challenged in chat.
- Faculty-feedback learning, ruling reuse/propagation and precedent learning are future scope. Case-specific decisions may be recorded without influencing other classifications.
- Tool diagnostics remain important; not every diagnostic function necessarily needs a separate model-callable tool.

## Knowledge and materials

- Operating Systems and Internet of Things are the initial subjects. The supplied populated trees are final resources for the build; faculty approval is not required. Uploaded syllabus/resource content becomes active/applied on the requested workflow after technical validation.
- Retain original syllabus structure, source text and IDs. Proposed enrichment adds boundaries, distinctions, contextual terms and internal assessed aspects.
- Uploaded teaching material is mapped across its extracted sections, with source citations, and applied additively on request without a second approval step. Conflicts and uncertainty must remain visible.
- Support common text, PDF, Office and image formats, including handwriting where extraction is reliable; do not promise perfect extraction or arbitrary format coverage.
- Specialized visual/OCR models may read scanned/image/handwritten documents, updating the earlier no-model-reading restriction.
- PaddleOCR-VL-1.6 through the official Hugging Face GGUF/Ollama path is selected for the initial OCR integration. Accuracy, memory use and correction effort still need measurement on actual notes and papers.
- Broad topic key points are reference knowledge, not mandatory answer requirements for every question.

## Hardware and efficiency

- User has 8 GB VRAM. A shared scheduler should coordinate all GPU runtimes and normally allow one model workload at a time.
- Process bounded batches, checkpoint progress, cache extraction and analysis, unload/release models before switching, and avoid per-page model swapping.
- Judge/helper can use one underlying model sequentially. CPU embeddings are a candidate starting point, subject to benchmarking.
- Gemma 4 12B is the selected shared judge/helper model, with both roles run sequentially. Its comparison quality and runtime configuration still need measurement on the target machine.

## Templates and output

- Separate paper-pattern templates, question-slot templates and result/report templates.
- Default and faculty/department custom templates; upload or describe a template, map fields, preview and save. Exact college patterns will be configured later from supplied samples.
- Export MD, TXT, PDF and XLSX, selected through chat/inline choices. Reuse structured results; changing presentation must not rerun classification.
- Template presentation cannot alter classifications or conceal incomplete results. Exact visual fidelity across output formats is not promised.
- Actual in-sem/end-sem patterns still require sample papers; do not infer full patterns from syllabus marks alone.

## Proposed stack from original spec

Python/FastAPI/Pydantic, PostgreSQL/pgvector, SQLAlchemy/Alembic, pgqueuer, LangGraph with separately testable functions; React/TypeScript/Vite, Tailwind/shadcn, TanStack Query, Framer Motion, GSAP, Cytoscape; choose one analytics chart library. Ollama default through a backend-neutral model client. Dependency versions have not been pinned or tested.

## Still unresolved

- Four OS and ten IoT interpretation questions are listed in the tree review files. They remain informational notes; they do not gate use of the supplied trees.
- Exact exam patterns, deployment arrangement, data confidentiality policy, model artifacts, supported runtimes, hardware profile and numerical release criteria.
- Score definitions/calibration and several audit recommendations need final decisions; suggestions in the transcript must not automatically be treated as approvals.
- The implementation now includes a local judge/helper comparison path, but no labeled benchmark result exists. Held-out family splits and real-material tests remain necessary before making robustness claims.

## Assumptions

This is a continuation summary, not a replacement final specification. When a detail conflicts with the original spec, use explicit later user decisions. Where the conversation only proposed an option, retain it as open.
