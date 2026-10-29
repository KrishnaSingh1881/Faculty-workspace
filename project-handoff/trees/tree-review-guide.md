# MSPA syllabus tree review

OS and IoT only. These are proposed enriched resources for review, not a claim of classifier robustness. No original attachment was edited.

## Start here

- Read `os-tree-review.md` and `iot-tree-review.md` for the complete readable trees.
- The matching JSON files contain the structured resources, original enrichment snapshots, provenance and change logs.
- Inspect the open questions first, especially ambiguous IoT source wording and OS printed hierarchy.

## Main changes

- Preserved all 167 source nodes, including IDs, hierarchy, labels, source wording and unit metadata.
- Added explicit node boundaries, question-sensitive task guidance and same-unit confusion-family distinctions.
- Moved cross-unit distinction entries into tagging-only disambiguation metadata.
- Repaired broad/narrow and partial-aspect aliases, including SJF/SRTF, paging/page tables, demand paging/virtual memory, sensors/actuators and LoRa/LoRaWAN.
- Added internal assessed aspects without changing the official tree: definition/characteristics, sensor/actuator, LCD/servo, service/level (provisional), communication models/APIs and digital/analog I/O.
- Replaced the inherited validated flag with needs_review and retained original provenance.
- Preserved original enrichment in each node so changes are inspectable.

## Review schema and integration

Schema `1.1-review` extends the original schema. An importer must explicitly support the new fields; these are not claimed to work in an existing application unchanged. No repeated product-release plan is introduced.

## Validation performed

Fresh checks verified unchanged protected fields, unique IDs, valid parents, no parent cycles, five units per course, descriptions within 45 words, valid distinction targets, same-unit enforcement and reciprocal distinction entries. Validation does not establish factual completeness or classification accuracy.

## Sources

- User-supplied syllabus PDFs, OS pages 18-19 and IoT pages 15-16 (PDF page numbering).
- User-supplied populated trees; prior textbook attributions are inherited, not verified quotations.
- https://lora-alliance.org/lorawan-for-developers/
- https://www.rfc-editor.org/info/rfc4944/
- https://aws.amazon.com/types-of-cloud-computing/
- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/5_CPU_Scheduling.html
- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/7_Deadlocks.html

## Assumptions

- Scope remains five units per subject, one unit per question and no cross-unit comparison.
- Teacher review/approval is not inferred from the prior validated flag.
- Official broad headings do not mandate every textbook example in every answer.
- Final model performance requires an independent OS/IoT benchmark; no classifier was run for this enrichment task.
