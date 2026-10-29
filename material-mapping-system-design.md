# Fast, reliable teaching-material mapping

## What changes

The current mapper makes a local LLM call for almost every PDF page. A 57-page slide deck therefore becomes roughly 57 slow requests, even though many slides are titles, continuations, or parts of the same syllabus topic. That is the wrong unit of work. The new unit is a **meaningful content block**: a heading plus its related slides or paragraphs, with every original page number retained for citations.

The chat should resemble a capable file assistant: acknowledge the upload, show what was extracted, show a few understandable live steps, then present the proposed syllabus mapping. Raw JSON, token fragments, and dozens of “thinking page N” entries do not belong in the main conversation. If the local model emits thinking, an optional collapsed detail can show it; the main feed shows what operation is happening and what it found. We cannot infer the private implementation of Claude or GPT from their interface, but this is the interaction the user asked for.

## Fast path

```mermaid
flowchart LR
  A["Upload and extract once"] --> B["Clean OCR and group related pages"]
  B --> C["Embed all blocks in one model session"]
  C --> D["Retrieve possible syllabus topics"]
  D --> E["Batch several blocks for local model verification"]
  E --> F["Validate citations and topic IDs"]
  F --> G["Show one reviewed mapping in chat"]
  G --> H["Apply selected tree changes"]
```

1. **Extract once.** Save the original file and page-level text. OCR only pages that lack usable text. Remove repeated headers/footers and flag unreadable passages. A title-only page joins the following content; it does not trigger a model call.
2. **Build content blocks.** Use headings, layout, neighboring pages, and topic transitions to group related content. Retain a `page → text span` map so a block covering several pages can still cite an exact page and quote. Split only when a block would exceed the model's token budget. Deduplicate repeated slide text.
3. **Retrieve candidates cheaply.** Run the selected local embedding model over all blocks together, then release it. Combine pgvector similarity with labels, aliases, unit hierarchy, and keyword matches. Use the union of signals for high recall; uncertain blocks get a wider candidate set. Do not send all 63 detailed IoT topics in every prompt.
4. **Use the LLM only where it adds value.** Batch several short blocks with their shortlist of candidate topics into one structured local-model request. The model checks whether each block actually supports the topic, drafts a short note, and returns exact source quotes. High-confidence direct label matches can be staged with their source text for review without asking the LLM to repeat a lookup. Ambiguous or conflicting blocks receive a focused follow-up. The number and size of batches are determined by token budget, not page count.
5. **Validate every result.** A mapping is usable only when its topic ID exists in the pinned tree version and its quote matches the cited page. Invalid individual items are rejected while valid siblings survive. No model-generated claim becomes mandatory syllabus wording. Conflicts and weak evidence stay visible.
6. **Assemble once.** Merge validated evidence for each topic, deduplicate notes and citations, and show one proposal per topic. The user edits or excludes suggestions, then explicitly applies the selected additive tree revision. The upload itself remains final; there is no separate faculty approval gate.

## Handling malformed or slow model output

- Use a JSON-schema response contract with a small, bounded output. Do not ask the model to describe all topics at once.
- If parsing fails, retry **that batch** once with a shorter prompt and thinking disabled. If it still fails, split the batch and retry the halves. Only the smallest failing block becomes `needs attention`; the rest of the document continues.
- A connection timeout uses bounded backoff. A persistent model outage pauses the run with a clear reason. Never report an unfinished run as “extraction ready” or “complete”.
- Save validated batches and their source hashes before moving on. After a restart, resume unfinished batches instead of starting at page 1. Cache keys include material hash, block hash, tree version, model, embedding model, prompt, and schema versions.
- Keep OCR, embedding, and LLM work in separate phases so the 8 GB GPU is not repeatedly switching models between pages. Run one GPU workload at a time.

## What the chat shows

During upload: **“I extracted 57 pages. Two need OCR review. Here is the text and document outline.”** The full extracted text stays available on demand.

During mapping: one compact live status, such as **“Finding syllabus topics for 12 content blocks”**, then **“Checking 4 ambiguous blocks with the local model”**. Show cache hits, retries, and issues as short events only when they occur. Keep detailed model thinking optional and collapsed; do not render a nested dashboard or scroll a line for every page/token.

At the end: a topic table with supporting page quotes, an uncertainty/issue count, and edit/exclude controls. If any block failed, call the result **partial**, show which blocks need attention, and offer a targeted retry. `Apply` affects only validated, included proposals and checks that the tree version has not changed.

## Durable records

Keep a mapping run (pinned versions and status), content blocks (page spans and extraction quality), batch attempts (status and errors), validated mappings (topic and exact citations), and a small structured event stream. Stream raw local-model thinking transiently if requested; persist only useful operation events and accepted evidence. A worker lease and heartbeat prevent an abandoned run from waiting 30 minutes after restart or being processed twice.

## Build order and verification

1. Replace page-by-page mapping with extraction cleanup, block grouping, and batch retrieval. Reuse the existing Qwen embedding and pgvector setup.
2. Add schema-constrained batch model calls, per-batch retry/split, and exact quote validation.
3. Add durable batch checkpoints and resume, then simplify the chat timeline and proposal review.
4. Run the real 57-page IoT PDF and compare against the old path: model calls, wall time, pages covered, valid citations, missed topic mappings, retry rate, and memory use. Also test malformed JSON, a title slide, OCR gaps, restart mid-run, and a changed tree. Do not set a fixed “calls saved” or accuracy claim before these measurements.

The current code has only partial safeguards and is **not** this design. The old 57-page run has been asked to stop; its upload and completed cached work remain available.
