# Faculty workspace

A local web application for syllabus-aware exam-question review. The approved Workspace concept is implemented as a React interface backed by FastAPI. The bundled OS and IoT trees load as active resources without a faculty approval gate; no classification accuracy claim is made.

## Run locally

This workspace currently contains locally cached Python and Node dependencies in `.venv` and `frontend/node_modules`. On a machine with package registry access, recreate them with:

```bash
uv sync --dev
cd frontend && npm ci && npm run build && cd ..
```

Install the three local Ollama models before starting the app:

```bash
ollama pull gemma4:12b
ollama pull hf.co/PaddlePaddle/PaddleOCR-VL-1.6-GGUF
ollama pull qwen3-embedding:4b
```

The installed local Ollama inventory includes Gemma 4 12B, PaddleOCR-VL-1.6 and Qwen3 Embedding 4B. Gemma text/JSON streaming and Qwen embedding inference have been exercised; full helper/judge classification and OCR quality still require evaluation. Set model variables in `.env` if you use different local tags. Judge and helper default to the same 12B artifact and run sequentially. Scanned pages and images use PaddleOCR-VL through Ollama; page batches hold the shared GPU lock and release OCR before other model work. Qwen uses the same lock for incremental question indexing and semantic searches. All model requests stay on a local/private Ollama endpoint and bypass HTTP proxies. Without the configured local models, extraction and classification report failures instead of substituting mock results.

Paper uploads preserve the full question text and also store a structured outline of prompt text, labeled subparts, explicit per-part marks, and detected OR choice groups. The Papers editor shows this detected structure and rebuilds it when the source text is edited; uncertain multi-part choice groupings are flagged for correction. The parser is heuristic, so verify the outline against uploaded source pages.

```bash
export JUDGE_MODEL_NAME='gemma4:12b'
export HELPER_MODEL_NAME='gemma4:12b'
export OCR_MODEL_NAME='hf.co/PaddlePaddle/PaddleOCR-VL-1.6-GGUF'
export EMBEDDING_MODEL_NAME='qwen3-embedding:4b'
export DATABASE_URL='postgresql+psycopg://faculty:YOUR_PASSWORD@127.0.0.1:5432/faculty'
.venv/bin/python -m uvicorn exam_assistant.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Startup applies versioned Alembic migrations before loading the workspace. PostgreSQL with the pgvector extension is the primary database and default connection; create the `faculty` database and credentials first, or use Compose below. For isolated tests or a single-machine fallback, explicitly set `DATABASE_URL=sqlite:////absolute/path/to/workspace.db`. For frontend development, run `cd frontend && npm run dev` and use Vite's URL. The API is documented at `/docs`.

## Docker Compose

Install Docker Desktop on Windows/macOS or Docker Engine and Compose on Linux. Run local Ollama on the host, install the judge/helper model tags, copy `.env.example` to `.env`, and replace the example database and administrator passwords. Then run:

```bash
docker compose up --build -d
docker compose logs -f workspace
```

Open `http://127.0.0.1:8000` and sign in with `ADMIN_EMAIL` and `ADMIN_PASSWORD`. PostgreSQL data and uploaded files persist in named volumes. The workspace port binds to loopback; for remote shared-host access, configure HTTPS and `COOKIE_SECURE=1` behind a reverse proxy, then restrict network access at the host firewall. The Docker image calls Ollama at `MODEL_URL` and does not include model weights.

On Linux, a host Ollama service that listens only on `127.0.0.1:11434` cannot be reached through Docker's host gateway. Use the included loopback bridge:

```bash
docker compose -f docker-compose.yml -f docker-compose.loopback-ollama.yml up --build -d
```

The bridge listens on Docker's host gateway at port 11435 and forwards to host loopback port 11434. It requires Docker Engine's Linux host networking and does not bind the model API to external host interfaces. On Docker Desktop, use the regular Compose command when `host.docker.internal:11434` is reachable from the workspace container. Check with `docker compose exec workspace python -c "import os,urllib.request; print(urllib.request.urlopen(os.environ['MODEL_URL']+'/api/tags',timeout=3).status)"`; a `200` means the model endpoint is reachable.

For a shared host, set `AUTH_MODE=shared`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` (12 or more characters) on first start and put the app behind HTTPS. Set `COOKIE_SECURE=1` behind HTTPS. Shared mode has administrator and teacher accounts, and teachers see only assigned subjects. Local mode is the default and runs as a local administrator without sign-in.

## Working flows

- Load the supplied OS and IoT trees as active resources, and import another five-unit tree directly. The bundled interpretation notes remain visible.
- Create papers or bulk import up to 20 files with per-file outcomes; extract text from PDF, Office XML, text and common image files; automatically tag questions when a model is configured, or edit tags directly. Uploads are stored immediately. Scanned pages and images use PaddleOCR-VL through Ollama and show manual-review warnings. A cross-process model lock serializes OCR, tagging, generation and comparison workloads.
- Preview exact same-unit comparison scope, run the sequential helper and judge roles on the configured Ollama model with callable syllabus, requirement and compound-alignment tools, cache outcomes by question revisions, tree version, model roles and tool/prompt/decision versions, and mark old verdicts stale. The model must be measured on the target machine; results remain provisional until a labeled benchmark passes. Accepted A/B/C public reasons are assembled by code from validated assessed-requirement mappings; judge prose remains in the evidence trace. Any displayed confidence is marked as an uncalibrated model self-report.
- Search indexed questions by meaning using Qwen3 Embedding 4B and exact pgvector cosine retrieval. Question and part vectors are indexed by a durable worker job after authoring or analysis changes; changing a question revision makes its old vector unavailable immediately. Semantic similarity supplies candidates and never decides A/B/C. A separate SQLite vector scan remains available only for isolated tests and local fallback.
- Follow live Workspace assistant, requirement extractor, helper and judge activity in the chat and comparison views. The interface shows actual Ollama thinking chunks when the model emits them, plus tool names, arguments, results and elapsed time. The local model selects a relevant tool family before each chat request, and broad searches return compact records so later tool calls remain grounded. When several returned records match a requested action, the latest chat answer offers clickable choices tied to exact search results. Conversation activity is saved so reopening a chat retains its trace. Use `MODEL_THINKING=true`, `false` or `auto` (default) to request the model's supported mode; reasoning text can be lengthy. `CHAT_CONTEXT_TOKENS` defaults to 8192 for the Workspace tool loop. `COMPARISON_CONTEXT_TOKENS` defaults to 8192 for requirement extraction and both comparison roles; adjust either after measuring the target machine. Context settings are included in pair cache invalidation.
- Generate editable draft questions from exact syllabus topics, unit, marks, difficulty and constraints. Generated candidates are screened by the same judge/helper comparison pipeline against selected references; screening remains provisional and does not claim novelty from a C result.
- Upload a sample paper to create an editable pattern suggestion from detected question counts and explicit marks; configure its syllabus slots and choice rules in Template Studio. Use five generic reusable comparison-scope presets, save validated paper/question/comparison/result templates; run scopes such as last-N references, within-paper checks and bank audits against current uploads; each run snapshots its scope and report layout. Apply ordered result columns to MD, TXT, PDF and XLSX exports, and map complete teaching documents across the syllabus with source quotes and cited topic notes.
- Delete papers, questions, materials and templates directly from explicit requests. Affected saved comparisons are removed, and an audit event records the deletion.
- Inspect results and recorded evidence in Results or ask chat to find a comparison, filter its saved pair results, and inspect an exact result. Chat can record a case note or resolve an exact review result without a second approval step; the ruling is audited and stays case-specific. Export saved comparisons as MD, TXT, PDF or XLSX. Ask the assistant to inspect recent background jobs, check job progress, or (as an administrator) retry failed jobs and cancel queued/running jobs; running work stops at safe boundaries. Administrators can also use Operations for workspace-wide queue and storage summaries. Interrupted comparisons can resume. Search the reference bank by phrase and unit, review the unit-by-year question heatmap and inspect repeated topics as historical counts (not predictions). Archive papers to exclude them from new comparisons while keeping them restorable.
- Run `python -m exam_assistant.benchmark labeled-pairs.json --split held_out` for a reproducible question-family held-out report, or `--split development` for development results. `benchmark-schema.example.json` shows the input shape; the corpus must be labeled before any accuracy claim.

## Checks

```bash
.venv/bin/python -m unittest discover -s tests -v
cd frontend && npm run build
```

## Current implementation limits

Background work is persisted in the database queue and resumes after a process restart. SQLite worker claims use a shared-volume lock; PostgreSQL claims use row locking. Local model workloads use a cross-process lock so OCR, embeddings and judge/helper calls do not contend for VRAM. With a local judge model configured, chat can call grounded tools for paper/question/syllabus/material/comparison/analytics lookup, semantic question search, paper and question creation/metadata edits, syllabus topic create/edit/delete and distinction links, archive and explicit deletion, template management, comparison lifecycle and case-specific result resolution/feedback, resource mapping, generation and report links. Chat can also inspect subject-scoped jobs; administrators can inspect all jobs, retry eligible jobs, cancel queued/running jobs, and request workspace operations summaries. Recent persisted tool results support follow-up references. Search results constrain exact edit/delete/job targets. The user interface presents tool activity and evidence as readable summaries rather than JSON. Chat uploads route through the same import handlers as Workspace uploads. Template-sample mapping creates an editable heuristic suggestion; it does not decide syllabus units or OR/choice logic. Full-document resource mapping checkpoints each validated section for retries, retains page quotes, and currently caps a job at 500 sections. Potential conflict flags show exact existing and uploaded-source quotes; they are prompts for review, not confirmed conflict rulings. PDF/OCR extraction still occurs during upload rather than as a resumable job. OS/IoT classification remains unmeasured until representative resources and an independently labeled held-out benchmark are available. Worker jobs can be cancelled before start or at the next safe boundary; interrupted comparisons can resume. Paper analysis reports mark distributions, unit marks share and unique current redundancy pairs; no uncalibrated health or predictability score is claimed. Question revision history captures create/edit/tag/tree invalidation events. Administrators can inspect worker/database/storage status, retry failed jobs, cancel queued/running jobs and download a full database-plus-uploads backup from Operations. Backup creation verifies that every referenced original upload exists and matches its content hash before publishing the archive (Ollama model artifacts are stored separately). To restore locally, stop the app, run `.venv/bin/python -m exam_assistant.backup restore /path/to/workspace-backup.zip` (Windows: `.venv\Scripts\python.exe -m exam_assistant.backup restore C:\path\workspace-backup.zip`), then restart. In Compose, keep PostgreSQL running, stop the workspace, and run `docker compose run --rm --no-deps -v /absolute/path/workspace-backup.zip:/restore.zip:ro workspace python -m exam_assistant.backup restore /restore.zip`, then start the workspace again. Restore requires a matching application schema and the same configured `DATABASE_URL`. Completed export files expire after 30 days by default; set `EXPORT_RETENTION_DAYS` to a positive number to change this. Job and audit records remain available after file cleanup, and an expired report can be queued again. Tested HTTPS proxy setup and complete corpus/OCR/model behavior checks remain open. The OS and IoT trees, uploads and explicit deletion requests do not require approval.
