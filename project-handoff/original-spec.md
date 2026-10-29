# MSPA: Spec

## 1. What it is

MSPA is a syllabus-aware exam question redundancy checker. It compares one corpus of questions against another, uses the syllabus to understand how topics relate, and says how redundant two questions are and why. It also scores a paper's health and generates fresh questions that avoid redundancy and keep predictability low.

Built from scratch. Runs locally. Papers are English only. Delivered as a web app (section 17), usable from one machine or a shared department host. Subjects are added through the app, not by hand. The main interface is a chat assistant, like Claude: a teacher says what they want, the assistant prepares it and shows exactly what will change, and one button click confirms.

## 2. The problem

Past exam papers are PDFs with no index. A paper setter cannot easily tell whether a question was already asked in an earlier year, whether two questions in the same paper test the same thing, whether one unit is over-tested, or how guessable the paper is.

Plain text or embedding similarity fails here. It matches different tasks on the same topic, confuses sibling topics, and misses rewording or negation. The decision depends on what the question asks and where its topic sits in the syllabus. So the checker must be syllabus-aware and meaning-aware.

## 3. Labels

MSPA compares questions from the same subject and the same syllabus unit. The corpus is already organised by subject and unit, so cross-subject comparison is out of the flow. The unit of a question comes from topic tagging, never from its question number. Tagging runs at the draft stage of ingestion, the teacher confirms the tags in the review step, and the unit is derived from the confirmed tags.

- **A: repeat.** Same concept, same task, same scope, same expected answer depth. Wording, examples, names, order or input values can differ.
- **B: related.** Meaningful shared content, but one question asks a different task, a broader scope, extra requirements, or a materially different answer depth. Also: partial overlap between compound questions, and one question containing the other ("contains" is a kind of B, not its own label).
- **C: unrelated.** No meaningful overlap in the concepts or requirements assessed.

Similarity scores and shared terms only help shortlist pairs. They never decide the label alone.

Examples:
- "Explain binary search with an example" / "Describe how binary search works, illustrating with an example": A (same task and scope, reworded)
- "Sort [3,1,2] using insertion sort" / "Sort [8,5,6] using insertion sort": A (inputs changed, same skill)
- "Explain binary search" / "Write the binary search algorithm": B (same concept, different task)
- "Explain binary search" / "Explain binary search, including time and space complexity": B (second adds requirements)
- A compound question sharing only one of its parts with another question: B (partial overlap)

Every A and B also records how the second question differs from the first: paraphrase, numbers changed, scope changed, task changed, reordered, merged, context swapped.

**Marks and depth.** Marks alone do not decide redundancy; what the student must produce does.
- Equivalent requirements with different marks: still A. The marks mismatch is reported as a paper-quality issue.
- The higher-mark question demands substantially more explanation, derivation, analysis or scope: B.
- A question with extra assessed requirements is not A just because its core topic matches.

**Compound questions.** A compound can be A only when all its parts align and the overall requirements and scope match. One exactly matching part never makes the whole compound A. Confirmed.

## 4. Syllabus knowledge tree

The syllabus is stored per course as a structured tree. It is a resource the agents and tools consult on demand, not a rulebook pasted into every prompt.

**Contents.**
- Nodes of four kinds: course, unit, heading, topic. Each has a stable path-style key (for example `2301202/u3/deadlock/prevention`) that is unique within a tree version and kept across versions, a parent, order, label and the original syllabus text. Patches, topic tags and staleness refer to this key.
- Per node, for headings and topics: a short description of what the topic is and where it stops; key points; synonyms and acronyms; scope terms and context words; links to sibling topics it is easily confused with and how they differ (each link carries a short note on how the two differ; links go both ways and stay inside the unit); optionally the kinds of tasks exams set on it.
- Per enriched node: who enriched it (model or teacher), its review status, and the terms the model was unsure of. Descriptions are at most 45 words.
- Per unit: teaching hours and the course outcomes it serves, with cognitive levels.
- Cross-links between topics with a confidence, plus provenance and a review status on every enriched node. Cross-links may cross units and are display-only (graph view, chat answers); they never affect a verdict.
- Topics are never compared across units; adjacency and distinguishing links are unit-local. The graph built from the tree treats adjacency as undirected, and every distance or neighbour lookup enforces the same-unit rule.

**Enrichment.** A bare tree gets a first enrichment pass per course from an external model (it can be re-run, see below), using one reusable prompt that works for any subject. The model returns patches only, keyed by node ID, never the whole tree. Per node a patch holds: description, key points, synonyms, acronyms, scope terms, context words, task types, uncertain terms, and distinguishing links (same unit, each with its how-note). Alongside the patches the model returns a list of syllabus issues (duplicates, misplaced topics).
- Stays within the syllabus. Anything it is unsure of, or any convention that differs between textbooks, is listed as uncertain, not asserted.
- Never changes protected fields (IDs, structure, labels, order, original text, unit metadata, existing cross-links, provenance, review). It may propose new cross-links, each marked "needs review".
- Never adds meta-commentary to descriptions.
- Every enriched node is marked "needs review" until a teacher approves it.

**Validator and merger.** Patches are checked and merged by code before use.
- Every node ID must exist; protected fields must be untouched.
- Merging is additive: existing keywords and links are kept, never deleted; only descriptions may be replaced.
- Distinguishing links are made reciprocal automatically.
- Descriptions stay within the length limit.
- The result is a new tree version; the old version is kept.
- A report lists rejected patches, unenriched nodes and syllabus problems the model spotted (duplicates, misplaced topics).

**Re-enrichment and editing.** The tree is a living resource, not a one-time import.
- Enrichment can be run again at any time, on the whole course, one unit or one topic. If the course already has enrichment, the app shows a warning and does not block.
- Any description, keyword or distinguishing note can be edited by hand. A manual edit is marked as the teacher's, and later enrichment never overwrites it.
- The tree can be exported and imported as JSON. An export package (the enrichment prompt plus the tree) goes to any external model, and the returned patches are imported through the same validator.
- Every change creates a new version. Versions can be compared and an earlier one restored.
- New or changed content shows "needs review" until a teacher approves it.
- A teacher can create or change any link (adjacency, distinguishing, cross) by telling the chat assistant in plain words. The assistant finds the topics, drafts the link and shows a confirm card; one click saves it. Links a teacher makes need no review and are marked as the teacher's. Adjacency and distinguishing links across units are refused, with the reason. Other tree edits work the same way.

**Adding a subject.** A teacher uploads the syllabus in any format. Ingestion (section 14) drafts the tree, the enrichment step fills it in, the teacher confirms. Teachers may import patches produced by any external model. A locally generated draft is expected to be rougher and goes through the same validator and review. Unit teaching hours and course outcomes are read from the syllabus text when present, otherwise entered by the teacher during onboarding.

## 5. How it works

1. **Ingest.** Parse the syllabus and papers, tag each question with syllabus topics, compute embeddings, run the per-question meaning tools once and cache the results.
2. **Prefilter.** Candidates are limited to the pairs the teacher's comparison selects (section 6) and to the same subject and unit. Pairs with no topic overlap and no neighbouring topics are C, with no LLM call. Topic neighbours are unit-local: adjacency is never inferred across unit boundaries.
3. **Shortlist and thresholds.** Lexical overlap, embedding similarity, topic overlap and cached meaning signals. Clear cases are settled by tuned thresholds. System default thresholds are set by evaluation on the synthetic corpus, and an institute can override them in its rules config.
4. **Agent loop.** Only uncertain pairs. A judge agent and a helper agent work together (section 7).
5. **Teacher review.** Pairs the agents cannot settle are flagged. A teacher's ruling is saved, outranks the agents, and applies automatically to the same pair or identical question texts. For similar pairs (same topic relation and same kind of difference, decided by code from stored fields, never by the model) the app offers to apply the ruling: it lists the pairs and the teacher approves all, some or none, and each applied ruling is logged as the teacher's decision. A teacher may switch on automatic application to similar pairs in their own skill or rules; this is recorded, and the hard rules stay fixed. Without that, earlier rulings on similar pairs are only shown to the judge as evidence.

Every verdict returns: label, confidence, short reason, evidence IDs, transformation, rounds used, whether it was flagged, and its source (threshold, agent loop, or teacher). It also records the tree, skills and rules versions it used. The current verdict of a pair is the teacher's ruling if there is one, otherwise the latest agent verdict that is not stale. Confidence is the weighted share of signals that support the final label, using signal weights from the rules config (system defaults set by evaluation).

**Review queue.** It holds flagged pairs, nodes needing review, ingestion drafts and generated questions. Any teacher of the subject can take an item, and one teacher's ruling applies for all.

## 6. Comparison scope and templates

Uploading a paper and comparing it are separate steps. Papers added to the corpus are never compared automatically. The teacher defines each comparison.

**A comparison has two sides.**
- **Targets:** the questions to check. The teacher picks a whole paper, specific question numbers, specific units, or ticks individual questions.
- **References:** what the targets are compared against. Any mix of uploaded papers (past, draft or bank), specific questions in them, or the whole bank for the subject. The same paper can be both target and reference, with an option to include or exclude comparison inside the target paper itself.

**Rules.**
- The subject and unit rules stay fixed. Only questions from the same subject and the same unit are compared. Selected questions in different units are not compared; they are listed as skipped with the reason.
- Per-question work (tagging, embeddings, meaning results) is done once at ingestion and does not depend on the comparison, so changing a comparison never recomputes it.
- Pair verdicts belong to the pair, not to the comparison. A pair already judged is reused by any later comparison that includes it, unless a version change made it stale.
- Everything shown (flagged pairs, health score, heatmap, trend) is scoped to the selected comparison. Predictability uses the selected references, and every report states which papers were used.
- Before running, the app shows the size of the comparison: pairs, skipped pairs, and how many will reach the agents. The teacher can narrow it first.
- A comparison can be started from the UI, from a template, or from the chat.
- A comparison runs as one background job for the whole selection, with visible progress, and can be resumed after a failure. Checking a single pair is an internal step, not a separate feature.

**Comparison templates.** A template is a saved set of rules for building a comparison, not a list of questions. It is applied to whatever papers the teacher has uploaded, so it is reusable every exam cycle. A template defines:
- targets, as a rule (the paper being checked, selected units, or selected question numbers)
- references, as a rule ("the last N papers of this subject", "all reference papers", "the bank", or named papers)
- options: include or exclude comparison inside the target paper, and an optional limit on how many past years to look back (which also sets the predictability window)
- the report template to produce when the run finishes

A template can decide only what is compared. It can never hide results or change the fixed rules.

**Starting templates.**
- Check my draft: the draft paper against all reference papers, including within-paper comparison.
- Draft against last N years: the same, limited to the most recent N papers.
- Within one paper only: duplicates inside a single paper.
- Selected questions only: the teacher picks the targets; references are all past papers.
- Whole bank audit: everything against everything, within the same subject and unit.

**Lifecycle.**
- **Making.** A teacher builds a template in a form in the comparison builder, copies and edits a default, describes it in plain words in the chat (the system drafts it and shows a preview), or imports a template file. Every template is checked by code against a fixed schema before it can be saved, and a template that tries to break the fixed rules is rejected with the reason.
- **Saving.** Default templates ship with the app. Teacher templates are stored in the database with a name, description, scope, owner and version number. Editing creates a new version and keeps the old one. Scopes follow skills: institute, department, course and faculty, with the more specific one winning unless a higher level locks it.
- **Sharing.** A teacher can publish a template to their department; an admin publishes at institute level. A template can also be exported as a file and imported on another installation. Imported templates go through the same checks.
- **Using.** The teacher picks a template in the comparison builder. The app resolves its rules against the papers actually present and shows the exact papers and questions chosen, plus the size of the run, before anything starts. The teacher can adjust the selection and run. The run is saved as a comparison record: template and version, resolved targets and references, who ran it, when, and the results. A record can be reopened, re-run after edits or version changes, and exported.

## 7. Agents

**Judge agent.** Decides the verdict. Its only actions are:
- ask the helper a question
- submit a verdict
- flag the pair for the teacher

**Helper agent.** An LLM that picks which data tools to call and returns facts only, never a verdict. This is what lets the judge check itself instead of agreeing with its first guess.

Redundancy checking uses these two agents. A supervisor agent above them is not built unless evaluation shows a gap the two cannot close; it is tested only as an optional experiment after the main evaluation.

**Generator agent.** Used only in question generation (section 11).

**Chat assistant.** Answers teachers' questions in plain language over read-only tools (section 15).

**Who does what.**
- Judge: owns the A/B/C verdict.
- Helper: investigates targeted evidence requests and returns grounded findings; never submits a classification.
- Deterministic code: enforces call limits, validates evidence references, applies hard constraints, computes confidence from configured signals.
- Teacher: resolves severe or persistent conflicts; rulings outrank automated verdicts.

**Loop.** The judge gets a compact initial bundle: question text, syllabus topic and unit, marks, task and depth signals, similarity signals. Each signal in the bundle is registered as an evidence item with its own ID, so a verdict with no tool calls can still cite them. If the case is clear it submits the verdict with no tool calls. If evidence is missing or contradictory it asks the helper to investigate that specific uncertainty, reassesses, and may ask again. Limits: 4 judge rounds, 6 helper tool calls per round. If a serious conflict remains, the pair is flagged for the teacher instead of forcing A, B or C. If the judge returns invalid output, the call is retried once with the error fed back; if it fails again, the pair is flagged for the teacher. A run never ends silently with no verdict and no flag; a run that fails shows as failed, with a retry action.

A syllabus-based result is not infallible. If strong contrary evidence appears, the judge investigates it. Straightforward pairs do not go through the loop.

**Grounding.**
- Every tool result gets an evidence ID.
- A verdict must cite evidence IDs; code rejects IDs that no tool returned.
- Confidence is computed by code from the evidence as a weighted combination using configured signal weights, not a plain count of agreeing signals and never taken from the model.
- Tool results are marked either computed by code or written by a model. Model-written results never override code-computed facts or syllabus facts.
- The helper cannot state syllabus facts that no tool returned.
- Everything is logged: prompts, tool calls, results, verdict.

**Models and backends.**
- Gemma 12B, temperature 0, model tag pinned and recorded. A local embedding model chosen by evaluation.
- One model-client interface. Ollama is the default; LM Studio and vLLM work through configuration. The pinned model record includes the backend and quantization, because results can differ between them. The evaluation is rerun on whichever backend ships.
- Replies must be forced into a defined structure (a valid tool call or verdict). Native tool calling is used if the backend supports it reliably; otherwise schema-constrained output.
- A startup check confirms the backend is reachable, the model is present, structured output works and temperature is zero.
- If the model backend is unavailable, MSPA says so and stops. It never substitutes a mock or canned answer.
- A cloud tier and OpenJev (a local fast scorer) are parked for later.

## 8. Tools

This list is a pool of candidate capabilities, not a build requirement. Use the smallest toolset that reliably improves outcomes: merge overlapping tools, drop any that does not measurably improve accuracy, efficiency or review quality, and keep deterministic checks for anything code can settle reliably. Build a small core first and add from this pool only when evaluation shows a gap.

Where a mature external tool already does a job (text extraction, OCR, file-type detection, text similarity), MSPA uses it. Models are used only for judgment and drafting.

All tools are deterministic code unless marked (model). Per-question tools run at ingestion and are cached. Per-pair tools run only inside the agent loop.

**Who calls what.** A tool is built only for the caller named here. Tools not named in the core are built later, only when evaluation shows a gap.
- **Helper, judge loop (core, 17):** `get_syllabus_unit`, `get_topic_neighbors`, `get_topic_relation`, `get_distinguishing_notes`, `get_question`, `get_question_topics`, `get_compound_segments`, `compare_intent_frames`, `check_subsumption`, `find_discriminating_differences`, `classify_transformation`, `get_signal_matrix`, `get_teacher_decisions`, `find_teacher_precedent`, `get_compound_structure`, `align_segments`, `get_segment_coverage`.
- **Code only, no model calls them:** the similarity signals (`lexical_overlap`, `embedding_similarity`, `topic_overlap`, `task_comparison`, `entity_diff`), which fill the judge's starting bundle; the per-question tools, which run at ingestion and are cached (core model tools: `extract_intent_frame`, `separate_context_and_ask`, `decompose_atomic_asks`, `extract_key_points`, `solution_method_signature`; core code tools: `get_constraints_and_modifiers`, `get_expected_answer_format`, `template_signature`, `canonicalize_terms`); and the scores. The helper reads cached results through `get_question`.
- **Chat assistant, read-only:** `resolve_topic_name`, `list_topics_in_unit`, `get_topic_path`, `get_topic_aliases`, `get_paper_coverage`, `get_question_history`, `get_question_family`, `get_predictability`, `get_level_estimate`, `get_paper_quality_checks`, `get_underused_topics`, `get_task_distribution`, `get_marks_budget`, `get_recent_questions`, `get_coverage_gaps`, `get_cluster`, `search_question_bank`, `list_skills`, `load_skill`, `get_active_rules`, plus the helper lookups. Two further tools only prepare a confirm card and change nothing: `propose_tree_change` and `propose_comparison`.
- **Generator:** `draft_question`, `find_similar_questions`, `get_coverage_gaps`, `get_underused_topics`, `get_recent_questions`, `score_draft_paper`.
- **Later, after evaluation:** `answer_outline`, `answer_equivalence_check`, `cross_answer_test`, `symmetric_judgment_check`, `compare_key_points`, `get_term_relation`, `get_shortest_path`, `get_related_topics_ranked`.

**Tool contract.** Every call returns an evidence ID, a source (code or model), the tool version, a status (ok or failed) and the result. A failed call still counts against the call limit, is never retried silently, and the caller is told it failed. Tools only read, except `propose_*`, which create a confirm card.

### Syllabus
- `get_syllabus_unit`: unit and position of a topic
- `get_topic_neighbors`: adjacent topics in syllabus order
- `get_topic_path`: unit, subunit, topic
- `list_topics_in_unit`: all topics in a unit
- `get_topic_aliases`: aliases and discriminating terms
- `resolve_topic_name`: free text to best-matching topics
- `get_topic_relation`: same, adjacent, related or unrelated, and why
- `get_distinguishing_notes`: how a topic differs from the siblings it is confused with

### Question
- `get_question`: text, paper, year, marks, parts
- `get_question_topics`: tagged topics with scores
- `get_compound_segments`: parts split from explicit labels, with topics and sub-marks

### Similarity
- `lexical_overlap`: token overlap and shared phrases
- `embedding_similarity`: cosine score
- `topic_overlap`: shared, neighbouring or none
- `task_comparison`: whether the asked tasks match
- `entity_diff`: which numbers or entities differ
- `find_similar_questions`: top matches within a chosen scope

### Meaning, per question (cached at ingestion)
- `extract_intent_frame` (model): concept, task, scope, expected answer shape
- `separate_context_and_ask` (model): scenario split from the actual ask
- `decompose_atomic_asks` (model): single asks inside a compound, used when it has no explicit parts
- `extract_key_points` (model): what a full-marks answer must contain
- `answer_outline` (model): short outline of the ideal answer
- `get_constraints_and_modifiers`: not, only, except, without using, for n inputs
- `get_expected_answer_format`: diagram, derivation, numeric, short note; depth from marks
- `solution_method_signature` (model): method a numeric problem needs
- `template_signature`: question with numbers and names blanked
- `canonicalize_terms`: wording mapped to syllabus terms

### Meaning, per pair (agent loop only)
- `compare_intent_frames` (model): compare by intent, not wording
- `answer_equivalence_check` (model): would one answer satisfy both
- `compare_key_points`: overlap of required answer points
- `find_discriminating_differences` (model): the smallest change that would alter the correct answer
- `check_subsumption` (model): does answering one answer the other
- `cross_answer_test` (model): grade each answer against the other question; asymmetry shows containment
- `classify_transformation` (model): how the second differs
- `get_term_relation`: synonym, broader, narrower, sibling, unrelated
- `get_signal_matrix`: every signal in one table
- `symmetric_judgment_check` (model): repeat the judgment with the pair swapped and report agreement

### Compound
- `get_compound_structure`: independent, dependent chain, or choose-any
- `align_segments`: part-by-part comparison table and best matching
- `get_segment_coverage`: how much of each side is matched

### History and precedent
- `get_question_history`: earlier papers with similar questions
- `get_teacher_decisions`: existing teacher ruling for a pair
- `find_teacher_precedent`: rulings on pairs with the same topic relation
- `get_paper_coverage`: questions and marks per unit
- `get_question_family`: chain of variants of one question across years

### Analytics
- `get_predictability`: score and its inputs
- `get_level_estimate`: cognitive level and difficulty
- `get_paper_quality_checks`: choice fairness, sub-part overlap, marks balance, answer leaks
- `get_underused_topics`: rarely or never tested recently
- `get_task_distribution`: how often each task type is used
- `get_marks_budget`: marks per unit against syllabus weight
- `get_recent_questions`: past questions on a topic, newest first
- `get_shortest_path`: path between two topics in the syllabus graph
- `get_related_topics_ranked`: related topics by graph proximity
- `get_cluster`: the redundancy cluster a question belongs to
- `get_coverage_gaps`: units or topics with few or no questions

### Bank, drafting, skills, rules
- `search_question_bank`: semantic search with course, unit, year, marks, level filters
- `score_draft_paper`: health score and components, recomputed on every change
- `list_skills`: index of available skills
- `load_skill`: full text of one skill
- `get_active_rules`: thresholds, constraints and relations for the active institute
- `draft_question` (model): generator only, drafts a question for a slot

### Judge controls
- `ask_helper`, `submit_verdict`, `flag_for_teacher`

`answer_outline` and `extract_key_points` overlap, as do `answer_equivalence_check` and `cross_answer_test`. Merge or drop after testing.

Later, not v1: `compare_with_cloud_judge`, `get_marks_weight`, `get_difficulty_hint`, `search_syllabus_text`.

Dropped: cross-unit relation tool (adjacency is unit-local). Also dropped as separate tools: `get_task_verbs` and `get_numbers_and_entities`; task verbs and numbers/entities are read inside `task_comparison`, `entity_diff` and the per-question tools.

## 9. Compound questions

A compound question is compared part by part.

1. Split into parts. Explicit labels ((a), (b), (c)) first; the LLM only when there are none.
2. Identify structure: independent parts, dependent chain (b uses a), or choose-any ("any 2 of 3").
3. Compare every part of one question with every part of the other. Each cell goes through the normal pipeline: prefilter, thresholds, agent loop only if uncertain.
4. Find the best one-to-one matching, weighted by sub-marks. Parts may stay unmatched.
5. Compute coverage in both directions.
6. Verdict (an exact match on one part never makes the whole compound A if the other question assesses additional requirements):
   - both sides fully matched, all A, structure aligns, overall scope matches: **A**
   - one side fully inside the other: **B, contains**
   - some parts shared: **B, partial overlap**, shared parts listed
   - nothing matched: **C**, or B if the topics are neighbours
7. Compound against a simple question uses the same method; a simple question matching one part gives B contains.
8. Questions sharing a scenario but asking different things are B at most.
9. The alignment is shown in the UI as links between parts.

## 10. Scores

- **Predictability (0 to 100).** How guessable a question is from past papers. Weighted blend of how often a similar topic and task appeared, how recently, how close the nearest past question is, and marks. Weights and lookback window are tunable. Always shown with its inputs. Computed as a weighted sum of the four signals, each scaled to 0 to 1; weights are equal until evaluation sets them.
- **Level and difficulty.** Six cognitive levels (remember, understand, apply, analyse, evaluate, create), from a task-verb table kept in the config. Difficulty is easy, medium or hard, from level, marks and number of parts.
- **Paper quality checks.**
  - OR-choice fairness: the alternatives in a choice differ in marks, level or difficulty beyond a set tolerance.
  - Overlap between sub-parts: an A or B verdict between parts of the same question.
  - Marks balance: a unit's share of marks against its share of teaching hours, within a set tolerance.
  - Answer leaks: one question's text contains the answer to another question in the same paper.
- **Health score.** Weighted blend of redundancy, predictability, level-mix match, marks balance and choice fairness. Components always shown. Weights come from the report template or a skill.

## 11. Question generation

1. Teacher sets the target: units, marks split, level mix, maximum predictability.
2. Blueprint of slots from coverage gaps and the target mix. A slot is a unit, marks, a level and a question type; slots fill coverage gaps first, then follow the marks split.
3. Generator drafts one question per slot, shown the nearest past questions to avoid.
4. Checker gate: the judge and helper compare the draft against past papers and the paper in progress, and predictability must be under the cap.
5. On failure the generator retries with the reason, up to 3 times, then escalates to the teacher with the reason.
6. Teacher accepts, edits or regenerates. A teacher has final approval. Accepted questions are saved as generated and join the question bank.

Every generated question must pass the same redundancy checker before entering the bank. It is also checked for: alignment with the intended topic, suitable difficulty and marks, acceptable redundancy against existing questions, and clear unambiguous wording. Factual correctness is a teacher check, since a small local model cannot verify facts reliably. A failed candidate is never accepted automatically.

The goal is to cut unhelpful repetition, not to remove every related question. A fixed syllabus limits the assessment space. B is not automatically bad: a related question is valuable when it assesses a meaningfully different requirement, depth or application. Coverage is never sacrificed just to lower a redundancy score.

"Replace with a fresh question" runs this for one slot copied from the question being replaced. MSPA recommends a replacement only when a flagged pair contributes to a real paper-quality problem (duplicated assessment, weak coverage, excessive predictability, unfair marks), explains the problem and suggests alternatives. Generated questions are never used as evaluation data.

## 12. Faculty skills and rules

**Skills.** Markdown files, like Claude skills. Each has a name, a one-line description, plain instructions and an optional settings block. Scopes: institute, department, course, faculty. The more specific scope wins unless a higher scope locks it. Agents always see the skill index and load the full text on demand. A teacher describes a preference in plain words; the system drafts the skill, previews how verdicts change on sample pairs, and the teacher approves. Skills cannot change the hard rules (evidence checking, caps, trust levels) or disable tools. A skill's settings block may only adjust soft preferences (for example tie-break leanings, weights within bounds, wording of explanations). The live preview re-runs the 10 judged pairs the skill affects most.

**Built-in skills.** MSPA ships a small set of default skills that faculty can copy and edit. They follow the same rules as any other skill. The set is defined during design.

**Rules config.** A per-institute file for thresholds, constraints (for example "repeated from the last two years is always A") and extra syllabus relations. Reaches agents through `get_active_rules`. A YAML file checked against a schema before it is accepted. System defaults (thresholds, signal weights, the task-verb table) ship with the app; the institute file holds overrides and ships empty in v1. College rules come later.

## 13. Reason log

Every verdict has two layers.
- **Short reason**: one line, for example "Same topic and task, numbers changed."
- **Full log** (expandable): signal table, cited evidence, transformation type, alignment table for compounds, skills and rules applied, model and prompt version, teacher ruling history, and a "what would change this verdict" line.

Built from structured evidence with fixed phrasing, not free LLM text. The short reason is produced by code from the structured fields (topic relation, transformation, signals), never written by the model. Rulings and re-runs add entries and never overwrite earlier ones. Shown in the UI and in exported reports.

## 14. Ingestion, corpus and storage

**Accepted input.** Syllabi and papers in any form: PDF (text or scanned), Word, Markdown, plain text, photos of printed pages, or text pasted with a line such as "this is the syllabus". Each upload carries course, year, semester and paper where known; missing details are asked for.

**Ingestion flow.**
1. Detect the file type and route it to the right extractor. Mature external tools do extraction and OCR; models are not used for reading text.
2. Draft the structure from the extracted text: a syllabus tree, or a paper's questions with marks, units, parts and OR choices. A model may help structure the draft. Topic tagging also runs here, so the teacher confirms tags and units in step 4.
3. Validate the draft by code (structure complete, marks add up, units known). Marks are checked against what a student actually answers: OR groups and "any n of m" count only the answered set, never the raw sum.
4. Show the draft beside the original for the teacher to confirm or fix. Nothing becomes official until a teacher approves it.
5. Store it, and run embeddings and the per-question tools. Tagging already ran in step 2; the teacher's confirmed tags are used.

Low-confidence extractions (poor scans, handwriting, complex math notation, odd layouts) are flagged for the teacher, never guessed. Extraction confidence is defined per extractor: OCR engines report their own scores, native-text PDFs count as high, and structure confidence comes from the validation in step 3.

**Upload safety.** Every upload is checked for size and real file type. OCR and conversion tools run sandboxed on untrusted files, with no access to stored data or credentials.

**Corpus management.**
- Mark each paper as reference (past), draft (under review) or bank. A draft becomes a reference only when the teacher promotes it (a button, used after the exam is held); only then does it count toward predictability and as a default reference.
- Duplicate upload (same file hash): rejected, with a pointer to the existing paper. Same subject, year, semester and paper number as an existing paper: warned, and the teacher chooses replace or keep both.
- Editing a confirmed paper: unchanged questions keep their IDs. Changed questions are re-tagged, re-embedded and re-run through the per-question tools. Verdicts involving them are marked stale, never deleted. Nothing re-runs by itself, because that costs model time; a "refresh" button re-runs what is stale. Teacher rulings on pairs whose question text changed are kept but marked "needs re-confirmation" and do not auto-apply until the teacher reconfirms.
- Re-ingest: produces a new draft beside the current version; nothing changes until the teacher confirms.
- Archive: hides the paper from pickers and excludes it from new comparisons and predictability. It stays visible in saved comparisons and history, can be restored, and keeps verdicts, rulings and traces.
- Delete: only for archived papers. If rulings or saved comparisons reference the paper, the teacher must confirm after seeing the list. Derived rows are removed and an audit stub records who deleted what and when. Rulings stay as stubs with a snapshot of the question text; saved comparisons show the paper as deleted.
- Bulk import: a manifest lists file, year, semester, paper number and status. Every file goes through the normal draft review. One failure does not stop the others, and a summary report is produced.
- Stale results after a tree, tool, prompt, skills or rules change are listed, and the "refresh" button re-runs them. Never automatic.
- Syllabus version history (section 4).
- Who may archive or delete follows the role permissions (section 17).

**What is stored in the database.**
- Subjects, tree versions and units.
- File records: content hash, type, uploader, time, where the original is kept.
- Papers and questions: text, marks, unit, parts and OR structure, extraction confidence, teacher-confirmed flag.
- Cached per-question meaning results, tagged with the tool version and model.
- Embeddings, tagged with the embedding model: one for the whole question and one for each part. The vector size depends on the model chosen, so it is set per model and not fixed in advance. Similarity search must work through pgvector for any supported model's dimension; at startup the app rejects an embedding model whose dimension the search cannot handle.
- Users and roles. Approvals and rulings reference the user who made them.
- Pairs that reached the judge: verdict, evidence IDs, confidence, which fields the model wrote and which the code computed.
- Trace events, teacher decisions, the review queue. Trace events are append-only, enforced by the database. Live notifications carry only the event ID, and the client fetches the event.
- Scores and report metadata.
- Run metadata: backend, model tag, quantization, temperature, prompt version, tool versions.
- Comparison templates with their versions, and saved comparisons with their resolved targets and references.
- Evaluation runs and ground truth.

**What is kept as files.**
- Raw originals, named by content hash, never edited.
- Exported reports.
- Faculty skills and the rules config, so they can be edited and version-controlled.
- Prompt templates.

**What is not stored.**
- Hidden model reasoning. Only structured events are kept; they are the audit record. Short text fields inside tool results (summaries, explanations) are kept as part of the trace, marked as written by a model, and never override code-computed facts.
- Individual rows for pairs the prefilter calls unrelated; they grow with the square of the question count. Only counts and reason codes are kept, and a pair is recomputed on demand.
- Anything cheap to rebuild once stale, such as embeddings after a model change.
- Student data, or any personal data beyond what sign-in needs. A user record holds an email, a display name, a role and a password hash, nothing else.

**Versioning.** Every derived result records the tree version, tool version, model, prompt version, skills version and rules version it came from. A change to any of them marks affected results stale so they can be re-run.

## 15. Chat assistant

Anyone allowed to use the app can ask questions in plain language, for example "Which Unit 3 questions repeat last year's paper?" or "Is Q4 too similar to anything in the bank?".

- The assistant picks read-only tools, runs them, and writes the answer from their results. Numbers and verdicts come from tool output with evidence IDs; the model only phrases them.
- If the data cannot answer ("will this paper be easy?"), it says so and offers the nearest thing MSPA can compute.
- Anything that changes data (approve a verdict, add to the bank, delete, export, edit a tree or a link) needs an explicit button click, never a sentence alone. The assistant prepares the change as a confirm card showing exactly what will change. A pending card expires after 7 days (a configurable value); an expired card is marked dismissed, not deleted. When a card is confirmed, the app first checks that what it targets has not changed since the card was drafted (for example a newer tree version); if it has, the card is marked stale and the assistant drafts it again.
- It can start a comparison from a request such as "compare Q3 and Q7 of the 2024 paper with the 2022 paper", showing the resolved selection for the teacher to confirm before it runs.
- Its tool calls and results stream into the live activity view (section 17).
- It never reveals content the user's role does not allow.
- Reliability is tested before the feature ships (section 19).

## 16. Demo features (all nine)

1. **Paper health report** from predefined templates that faculty choose.
2. **Click a flagged pair** to see why: label, reason log, evidence, trace. Compound pairs show alignment links.
3. **Replace with a fresh question**, suggested when a flagged pair causes a real paper-quality problem, with predictability before and after.
4. **Coverage heatmap**: units by years.
5. **Predictability trend** across years.
6. **Live faculty skill**: add a one-line preference and watch verdicts change.
7. **Exportable report** in the chosen template.
8. **Question bank search** with filters across all papers and years.
9. **Draft paper builder** with a live health score.

**Report templates (starting set, contents to confirm):** Quick duplicate check; Exam committee summary; Department view; Moderator checklist.

## 17. Web app and UI/UX

**Form factor.** A web app, served from the local machine or a shared department host. A desktop wrapper can be added later around the same app; it is not a separate build.

**Interface.** The chat assistant is the main way to work. Teachers say what they want in plain words (compare these papers, link these topics, archive this paper); the assistant prepares it, shows a confirm card, and one click makes the change. The other surfaces below are for looking at results and for the same actions by hand.

**Layout (workspace style).**
- Left: papers and tasks with run status and progress.
- Centre: the live activity view and the chat.
- Right: review panel for the selected pair, with the two questions side by side, the verdict, cited evidence and accept, override or flag actions.
- Further surfaces: corpus manager, comparison builder with template picker, graph view, heatmap and trend, review queue, generation panel, bank search, draft builder, skills editor, report page, subject onboarding with the original shown beside the extracted draft.

**Live activity view.** Streams what the system is doing as it happens: judge rounds, helper tool calls, evidence IDs returned, final verdict. Each step has a short plain-language caption, a running timer and an expandable detail. It shows real trace events, never invented "thinking" text, and the same events are the stored audit record.

**Visual design.**
- Dark and light themes from the start, built on design tokens. Defaults to the system setting and remembers the user's choice.
- Status colors (repeat, related, unrelated, flagged) must stay distinguishable in both themes and never rely on color alone.
- Animation: Framer Motion for interface transitions and list changes; GSAP for longer timelines or scroll-driven sequences. Only transform and opacity are animated, and the system's reduced-motion setting is respected.
- shadcn/ui as the base component set. React Bits components are used only for accents (headers, empty states, live-view entrances) after their license and theme support are confirmed. Data-heavy screens (review, reports) stay plain and fast.

**Access.** Two roles in v1. A teacher can do everything except user management, settings and institute-level publishing: rule on flagged pairs (any teacher of the subject), edit trees, manage papers, publish templates to their department. An admin manages users, settings and institute-level publishing. Faculty is a skill scope, not an account type. There is no student role in v1. Roles are stored as configuration, so finer roles can be added later. Local single-user mode is a configuration flag that runs as admin with no sign-in; it is never inferred from the connection. Sign-in and user and role management are part of the build. Every screen has a matching API.

## 18. Tech stack

Fixed now so features added later do not force replacing a layer.

- **Backend:** Python 3.12+, FastAPI, Pydantic v2, live events over server-sent events.
- **Agent orchestration:** LangGraph, version pinned. Judge, helper and validator steps are plain, separately testable functions that the graph calls.
- **Models:** one model-client interface; Ollama default, LM Studio and vLLM by configuration (section 7).
- **Database:** PostgreSQL with pgvector; SQLAlchemy 2 and Alembic migrations.
- **Job queue:** pgqueuer, using its own tables, for ingestion and long runs, with retries and visible status. No hand-written queue table.
- **Files:** content-addressed local file store for raw originals.
- **Frontend:** React, TypeScript, Vite, Tailwind, shadcn/ui, TanStack Query, a typed client generated from the OpenAPI schema.
- **Ingestion:** PyMuPDF and pdfplumber for text PDFs; Docling or Marker for layout; Tesseract with PaddleOCR or Surya for OCR; OpenCV and OCRmyPDF for scans; python-docx and Pandoc for Word; python-magic for file-type detection. The OCR engine, layout extractor and embedding model are chosen by a short test on real papers.
- **Similarity:** embeddings through the model server, rapidfuzz, scikit-learn, spaCy, optional reranker.
- **Graph:** NetworkX for paths, clusters and gaps. No GNN. The graph view in the browser is drawn with Cytoscape.js.
- **Reports:** python-docx or docxtpl for Word, WeasyPrint for PDF, Plotly or Recharts for charts.
- **Quality:** pytest, ruff, mypy or pyright, pre-commit, GitHub Actions CI, Playwright for end-to-end UI tests.
- **Observability:** structured logs and OpenTelemetry; the database trace is the audit record. Langfuse is optional.
- **Packaging:** Docker Compose for the full stack, with a documented install path for machines without Docker.

## 19. Test data and evaluation

No labelled data exists. The syllabus is the only real input. Papers are synthetic, generated by Krishna with Claude and GPT from the syllabus, with every planted case recorded in a ground-truth file.

**Subjects.** Operating Systems, whose tree is built and enriched first, and IoT, added through the app's onboarding flow with no manual tree work. Together they test the checker and the portability of the whole path (upload, ingestion, tree creation, checking). Remaining subjects are then added through the app as further portability tests.

**Corpus:** 4 to 5 exam years with 1 to 2 papers each per subject, in a realistic college format, plus one draft paper with planted problems.

**Files:** `papers/<year>_<n>.json`, `draft_paper.json`, `ground_truth.json`.

**Planted cases:** A, B, C pairs; compound cases (full alignment, partial, subset, reordered, shared scenario, dependent chain, choose-any); hard negatives (sibling topics, heavy word overlap with different tasks); negation traps; paraphrase depth 0 to 4; predictability bands; level mix; quality problems in the draft; coverage extremes; bank search targets; draft-builder swaps.

**Labelling:** one model generates, a second labels a sample, a human spot-checks about 50.

**Compared configurations:** thresholds only, single model call with syllabus context, judge and helper loop.

**Metrics:** precision and recall separately for A, B and C; confusion matrix and error breakdown by case type; compound alignment accuracy; teacher-escalation rate; time and tool calls per pair; citation validity; run-to-run consistency; and feature checks against ground truth.

**Additional checks.**
- Ingestion: extraction accuracy on typed, scanned and photographed inputs, and how often the teacher has to correct the draft.
- Tree enrichment: validator pass rate and teacher edit rate, for externally enriched and locally drafted trees.
- Chat: about 50 realistic teacher questions with the expected tool and answer, measuring tool choice, grounded answers and refusal when data cannot answer.
- Backends: the same suite on each supported backend; Gemma 12B native tool calling checked here.
- Optional: a supervisor agent against the two-agent loop.

Do not pick the architecture on overall accuracy alone. Missing a real repeat and falsely flagging an unrelated pair have different consequences. The loop stays only if it beats the single call. Synthetic results show performance on that test set, not on real exam papers.

Principle: keep the system as simple as possible but no simpler than the evidence requires. Tools and stack choices are fixed up front; individual features and tools are added only when evaluation shows a need.

## 20. Rules for the documents built from this spec

This spec is turned into requirements, design and tasks. These rules keep those documents from guessing.

- If the spec does not decide something, the documents list it as an open question. They never choose silently.
- Each document ends with an "Assumptions" list naming every choice it made that the spec did not state, so it can be reviewed.
- Tests are mandatory, not optional. A property test that checks a stored value compares it with a fresh recomputation from the current state.
- The synthetic corpus is produced outside the app (section 19). The build includes a loader, a validator and a ground-truth schema, not a corpus generator, and they come before the agent-loop checkpoint.
- Each of these has a requirement, a design element and a task: tree keys and links, re-enrichment and editing, ruling reuse, comparison templates and saved comparisons, paper-level runs, heatmap, trend and graph view, replace with a fresh question, draft builder, skills and rules, users and sign-in, tree import and export, upload safety, the corpus manager, the tool table (caller, core or later, failure), and confirm cards.
- Prompt text is supplied separately from these documents. The design lists the output format of every model step (a "model output contracts" section). The build includes a loader that reads versioned prompt files, records each prompt's version in every run, and marks results stale when a prompt changes.
- A backend test checks Gemma 12B native tool calling on each supported backend.

## 21. Open questions

1. Paper format for Operating Systems and IoT (units, marks per question, OR choices). Needed before generating the corpus. The IoT syllabus and sample papers are needed as input.
2. Does the Gemma 12B build support native tool calling on the chosen backend?
3. Report template contents and export format?
4. Predictability weights, confidence weights and lookback window? (Initial values come from evaluation.)
5. Deployment target: one teacher's machine or a shared department host? (Postgres is chosen so both work.)
6. Are unreleased papers confidential? If so, encryption at rest and access logging.
7. May enrichment include textbook-standard terms outside the syllabus (marked as such), or strictly syllabus-only?
8. Which built-in skills ship?
9. Are the desktop wrapper and Langfuse wanted, and when?

Settled: teacher rulings apply automatically to the same pair, are offered for confirmation on similar pairs, and can be set to apply automatically to similar pairs by the teacher (section 5); enrichment is a first pass that can be re-run at course, unit or topic level and edited by hand, and links can be made through the chat assistant (section 4); comparisons are teacher-defined and run from reusable templates (section 6); the tool table says who calls what and which tools are core (section 8); corpus manager rules (section 14); two roles, teacher and admin, with any teacher of the subject ruling on flagged pairs (section 17); prompt text is supplied separately (section 20); labels stay A/B/C; "contains" is a kind of B; a compound is A only when all parts align; adjacency is unit-local; web app first; two agents to start; no mock model fallback.