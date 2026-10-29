# Faculty Workspace

## A smarter way to understand, compare and prepare examination papers

**Faculty Workspace is a local AI assistant for examination work. It brings a subject's syllabus, past papers, question comparisons, draft generation and reports into one place—so faculty can spend less time searching through documents and more time exercising academic judgment.**

It is designed around a simple idea: a question paper is more than a collection of sentences. Each question belongs to a subject and unit, assesses one or more ideas, and asks students to demonstrate a particular level of understanding. Faculty Workspace brings those details together when it helps review a paper.

---

## The pitch in 30 seconds

Every examination cycle, faculty revisit old papers, check syllabus coverage and look for questions that may be repeated or too similar. That work is important, but it is scattered across PDFs, spreadsheets and individual memory.

Faculty Workspace turns that scattered material into a searchable, syllabus-aware workspace. Upload papers, check extracted questions, compare them against past papers and see the judge's reason directly in chat. When preparing a draft, ask the assistant to generate questions and screen them against prior papers. Export the saved comparison results into a report for further review.

The system can run with local models and gives the faculty member access to the questions, evidence and uncertainty behind each result.

---

## The problem worth solving

Preparing a good examination is a demanding academic task. Faculty must balance syllabus coverage, marks, clarity, difficulty and the depth of the task being asked. At the same time, they need to know what has appeared in earlier papers.

In practice, this creates several problems:

- **Past papers are difficult to navigate.** Relevant questions may be spread across many PDFs, scans or spreadsheets.
- **Wording hides similarity.** Two questions can assess the same idea with different phrasing, while questions sharing a keyword may ask for very different work.
- **Context matters.** A result makes more sense when the comparison respects the subject, syllabus unit, topic and instruction verb.
- **A label alone is not enough.** Faculty need to see the base question, the past-paper evidence and the reason for a classification.
- **Generating a draft creates another review cycle.** New questions still need to be checked against the syllabus and previous papers.
- **Administrative work interrupts academic work.** Extraction, organizing questions, tracking progress and preparing reports are all necessary, but consume time.

Faculty Workspace addresses these needs as one connected workflow.

---

## The solution

Faculty Workspace provides a conversational interface backed by structured academic data and local AI models. It helps faculty move from a collection of documents to a reviewable examination workflow:

1. **Bring in the syllabus and papers.** Store subject units and topics, upload papers and extract their questions.
2. **Review and correct the data.** Inspect extracted wording and confirm or edit question tags.
3. **Compare with context.** Select a base paper and past papers; the system checks each base question against the appropriate unit block.
4. **Understand the decision.** Read the classification, base question and reason in chat; expand the supporting past-paper block and evidence.
5. **Create a draft.** Generate questions for selected syllabus material and screen them against available references.
6. **Share the outcome.** Use `/report` to export comparison results saved in the conversation.

The result is an assistant that helps faculty review their own material with context and traceable reasons.

---

## What makes the project special

### 1. The syllabus is part of the workflow

The workspace organizes questions around subjects, units and topics. This gives faculty a meaningful way to navigate their question bank and keeps paper comparisons focused on the relevant unit.

The syllabus is also useful during generation: a candidate question is drafted for a selected unit and topic, rather than being produced as a generic exam question.

### 2. It checks a question against a whole unit block

A base question may be answered by content in one past sub-question, split across several sub-questions or combined with another topic. Faculty Workspace sends the judge the relevant past-paper unit block so it can consider the full context.

This also changes the amount of work required. For example, comparing two 12-question papers with six questions in each of two units can involve 72 same-unit question pairs. A block-based paper comparison instead performs 12 base-question checks against the relevant blocks. Each check still requires model work, but the workflow avoids a separate judgment for every pair.

### 3. It considers topic and depth

The comparison prompt asks two practical questions:

- **Topic:** Does the core topic appear anywhere in the past-paper block?
- **Depth:** When the topic appears, is the assessed coverage complete, and do the main instruction verbs fall in the same configured group?

The resulting labels are:

| Label | Intended interpretation |
| --- | --- |
| **A** | The topic is fully covered with the same configured instruction-depth group. |
| **B** | The topic appears, but coverage is partial or the instruction depth differs. |
| **C** | The core topic is absent from the whole selected unit block. |
| **Needs review** | The system cannot confidently accept the result under its checks. |

The judge is prompted to identify a concrete missing or changed ask when it selects B. C remains tied to absence of the core topic from the block.

### 4. The reason is visible where the work happens

A classification is most useful when a person can challenge it. Each result card shows the base question, the label and the recorded reason directly in the conversation. The user can expand the past-paper block and evidence to inspect what was used.

This makes the output a starting point for faculty review, not an unexplained score.

### 5. The judge leads; a helper is used selectively

The normal unit-block path uses the judge to make the assessment. Code checks the response format, the cited question numbers and recognized instruction-verb groups. When a response is unclear or fails a check, an independent helper can be consulted and the judge can reconsider it. If uncertainty remains, the result is marked for review.

The design aims to reduce unnecessary model calls while preserving an escalation path for difficult cases.

### 6. Draft generation is connected to past papers

A generated question should be checked in the same context in which it will be used. The generation flow receives the chosen syllabus topics and selected past questions. It then screens candidates against the relevant past-paper blocks.

The InSem shortcut currently creates a draft of **20 questions: ten from Unit 1 and ten from Unit 2**, with four marks per question as the configured default. The generator can try alternative candidates when the checks return A or need review. It reports the actual outcomes instead of claiming that a particular distribution is guaranteed.

### 7. Local models support a controlled deployment

The project is built to work with a local or private Ollama endpoint. Its configured roles include a language model for judging and drafting, an OCR model for scanned material and an embedding model for semantic search. A shared model lock helps coordinate workloads on the local machine.

This architecture is useful for institutions that want more control over where their working material and model requests are processed. The actual privacy and security properties depend on deployment and configuration.

### 8. Results become reusable records

Questions, classifications, reasons, evidence and job status are stored as structured records. The chat can reconnect to a saved comparison, and `/report` can package results saved in the current conversation. The Excel report presents papers side by side, classification counts and a separate reasons sheet.

---

## A simple demonstration story

**Scenario:** A faculty member wants to review an Operating Systems InSem paper against a previous paper.

1. Open Faculty Workspace and select **Operating Systems**.
2. Upload the base and past papers. Review the extracted questions and correct any topic tags that need attention.
3. Type **`/compare`**, choose the base paper, past paper and comparison pattern, then preview the scope.
4. Start the comparison. Watch progress in the chat as unit-block results arrive.
5. Read a result card: the base question, its A/B/C or review status, and the reason are visible together. Expand the past-paper block when more context is needed.
6. Type **`/report`** to download the comparison results saved in that conversation.
7. For a new draft, type **`/generate insem`** and review the generated questions and screening outcomes.

This demonstration shows the complete path from source material to an explainable, exportable review.

---

## Benefits for faculty and institutions

### For faculty

- Find and review relevant questions in the context of their subject and syllabus.
- See why a question was classified, with the source text available for inspection.
- Spend less effort assembling comparison information manually.
- Generate editable draft questions and see how they relate to selected past papers.
- Keep results and reports connected to the conversation in which the work happened.

### For departments and institutions

- Build a more organized body of past examination material.
- Give faculty a consistent workflow for comparing and reviewing questions.
- Preserve evidence and reasons alongside saved outcomes.
- Run the system using locally configured models and infrastructure.
- Extend subjects, syllabus trees, templates and evaluation datasets as institutional needs grow.

These are intended benefits of the workflow. The scale of time savings and classification quality should be measured with faculty and representative papers.

---

## The technology behind the experience

| Component | Role |
| --- | --- |
| **React and TypeScript** | Browser-based faculty workspace and conversational interface. |
| **FastAPI and Python** | Application API, validation and orchestration. |
| **PostgreSQL and pgvector** | Persistent workspace records and vector-backed search in the primary deployment. |
| **Ollama** | Local model runtime for configured judge, helper, OCR and embedding roles. |
| **Document extraction and OCR** | Turn uploaded documents and scanned pages into reviewable text. |
| **Background jobs** | Track longer tasks, progress, cancellation and retry states. |
| **Excel and text exports** | Package saved results and reasons for review outside the application. |

At a high level:

```text
Faculty member
      ↓
Chat and workspace interface
      ↓
Application API and background jobs
      ↓
Syllabus + papers + saved evidence  ↔  Local AI models
      ↓
Comparison results, draft questions and reports
```

---

## What has been demonstrated

The prototype has been exercised with Operating Systems papers in the local workspace. A browser run compared two 12-question papers using 12 unit-block checks and completed in **34.4 seconds** under the classifier configuration used for that run. Later prompt and validation changes mean that figure is an observation, not a current performance guarantee.

The project also has automated tests covering core workflows including tagging, comparison, generation, conversations and reports. A recorded run passed 24 tests. Tests demonstrate specific software behavior; they do not establish the semantic accuracy of the local model.

The draft-generation workflow has also been run locally, including screening generated questions against past papers. Local hardware limits can affect duration and availability, and model failures must be handled through retry or review.

---

## Responsible use and current boundaries

Faculty Workspace is a working prototype and a decision-support tool. Its strongest position is transparency: it provides the question, classification, reason and evidence so a faculty member can assess the output.

- Classification results are **provisional** until evaluated against a faculty-labeled benchmark.
- A C result means the classifier found the core topic absent in the selected block; it is not proof of novelty or quality.
- OCR and document extraction can make mistakes, especially with scans, diagrams, equations and technical notation.
- Questions and tags should be checked against their source papers.
- Generated questions require academic review for correctness, syllabus fit, marks and choice structure.
- Runtime depends on the machine, model configuration, number of past papers and whether retries are needed.
- The Excel export follows the reference's side-by-side reporting idea; it does not yet reproduce all formulas, charts and sheets in the example workbook.

These boundaries are opportunities for rigorous evaluation and product development.

---

## Where the project can go next

1. **Faculty-led evaluation:** build a labeled question set and measure accuracy, disagreement, review rates and time saved.
2. **Broader academic coverage:** onboard more subjects, syllabuses and institution-specific paper patterns.
3. **Better document understanding:** evaluate extraction across scans, figures, tables and mathematical notation.
4. **Stronger paper design assistance:** refine marks, choice groups, coverage and difficulty in generated drafts.
5. **Richer reporting:** add validated formulas, charts and additional workbook structures where faculty need them.
6. **Deployment readiness:** expand accessibility, recovery, security and shared-host testing.

---

## Why this project matters

Faculty Workspace brings together the information faculty already rely on—syllabuses, past papers and their own academic judgment—and makes it easier to work with that information in one place. Its value is the combination: subject context, question-level review, reasons that can be inspected, assisted drafting and reports that follow the conversation.

The project is a foundation for a more informed examination workflow: one in which AI helps surface useful evidence and faculty remain responsible for the final paper.
