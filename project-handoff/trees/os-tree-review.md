# Operating Systems: enriched tree for review

Status: needs your review. Original syllabus structure and source text are preserved. Added distinctions and assessed aspects are proposed enrichment. Classification performance has not been tested.

Course: 2301202 | Syllabus: KKW-AIDS-2023

## Review decisions needed

- **Contiguous memory allocation techniques:** The printed hierarchy groups paging and segmentation under contiguous allocation. Preserve it as a source outline, not an is-a taxonomy.
- **Translation lookaside buffer:** TLB appears in the printed page-replacement list; it is an address-translation cache, not a replacement algorithm.
- **Shortest job first:** Confirm whether in-syllabus SJF questions include SRTF; never assume the variant when a problem is underspecified.
- **Single pass assembler:** Confirm the prescribed forward-reference handling scheme and terminology; supporting implementation details are not universal requirements.

## How to read this tree

Descriptions identify the topic. Boundaries separate nearby concepts. Distinction notes do not imply A, B or C. Supporting examples are optional context, not requirements for every answer. Every enrichment remains needs-review.

## Introduction to systems programming

ID: `2301202/u1`

**Original syllabus:** Unit I Introduction to systems programming (07 Hrs) CO1

Hours: 7; outcomes: CO1.

### Introduction to system software

ID: `2301202/u1/introduction`

**Original syllabus:** Introduction

What system software and systems programming are, and how they differ from application software.

**Scope:** What system software and systems programming are, and how they differ from application software.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** systems programming, system software

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Components of system software

ID: `2301202/u1/components`

**Original syllabus:** Components of System Software

The pieces that make up system software and how they cooperate.

**Scope:** The pieces that make up system software and how they cooperate.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** components of system software

**Reference points:** language processors; program generation and execution

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Text editors

ID: `2301202/u1/text-editors`

**Original syllabus:** Text editors

Line, stream and screen editors and their structure.

**Scope:** Line, stream and screen editors and their structure.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** text editor, editors

**Reference points:** line editor; screen editor; editor structure

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Loaders

ID: `2301202/u1/loaders`

**Original syllabus:** Loaders

Programs that load object code into memory; absolute and relocating loaders.

**Scope:** Place executable code in memory and prepare execution.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** loader

**Reference points:** absolute loader; relocating loader; bootstrap loader

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Linkers:** Loaders: Place executable code in memory and prepare execution. Linkers: Combine object modules and resolve external references. Shared family membership alone does not establish assessed overlap.
- **Compared with Compilers:** Loaders: Place executable code in memory and prepare execution. Compilers: Translate high-level source; overview of translation phases. Shared family membership alone does not establish assessed overlap.
- **Compared with Macro processors:** Loaders: Place executable code in memory and prepare execution. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.

### Linkers

ID: `2301202/u1/linkers`

**Original syllabus:** Linkers

Combining object modules and resolving external references; relocation.

**Scope:** Combine object modules and resolve external references.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** linker, linking

**Reference points:** relocation; external references; static vs dynamic linking

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Loaders:** Loaders: Place executable code in memory and prepare execution. Linkers: Combine object modules and resolve external references. Shared family membership alone does not establish assessed overlap.
- **Compared with Compilers:** Linkers: Combine object modules and resolve external references. Compilers: Translate high-level source; overview of translation phases. Shared family membership alone does not establish assessed overlap.
- **Compared with Macro processors:** Linkers: Combine object modules and resolve external references. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.

### Assemblers (as system software)

ID: `2301202/u1/assemblers-overview`

**Original syllabus:** Assemblers

The assembler's role among system software components, at overview level.

**Scope:** The assembler's role among system software components, at overview level.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** assembler

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Assemblers:** the assembler's place among system software, not its design

### Macro processors

ID: `2301202/u1/macro-processors`

**Original syllabus:** Macro processors

Macro definition, macro calls and macro expansion.

**Scope:** Expand macro definitions at calls; not runtime function execution.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** macro processor, macros

**Reference points:** macro definition; macro call; macro expansion

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Loaders:** Loaders: Place executable code in memory and prepare execution. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.
- **Compared with Linkers:** Linkers: Combine object modules and resolve external references. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.
- **Compared with Compilers:** Compilers: Translate high-level source; overview of translation phases. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.

### Compilers

ID: `2301202/u1/compilers`

**Original syllabus:** Compilers

Translating high-level programs into machine code; phases of compilation at overview level.

**Scope:** Translate high-level source; overview of translation phases.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** compiler

**Reference points:** phases of compiler; lexical analysis; code generation

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Loaders:** Loaders: Place executable code in memory and prepare execution. Compilers: Translate high-level source; overview of translation phases. Shared family membership alone does not establish assessed overlap.
- **Compared with Linkers:** Linkers: Combine object modules and resolve external references. Compilers: Translate high-level source; overview of translation phases. Shared family membership alone does not establish assessed overlap.
- **Compared with Macro processors:** Compilers: Translate high-level source; overview of translation phases. Macro processors: Expand macro definitions at calls; not runtime function execution. Shared family membership alone does not establish assessed overlap.

### Debuggers

ID: `2301202/u1/debuggers`

**Original syllabus:** Debuggers

Tools that let programmers inspect and control running programs.

**Scope:** Tools that let programmers inspect and control running programs.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** debugger

**Reference points:** breakpoints; single stepping

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Assemblers

ID: `2301202/u1/assemblers`

**Original syllabus:** Assemblers:

Assembly language and the design of one-pass and two-pass assemblers.

**Scope:** Assembly language and the design of one-pass and two-pass assemblers.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** None asserted.

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Assemblers (as system software):** Consult the distinction from Assemblers (as system software): the assembler's place among system software, not its design

### Elements of assembly language programming

ID: `2301202/u1/assemblers/elements-of-alp`

**Original syllabus:** Elements of Assembly Language Programming

Statement format, mnemonics, operands and the kinds of assembly statements.

**Scope:** Statement format, mnemonics, operands and the kinds of assembly statements.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** elements of assembly language, assembly language programming

**Reference points:** imperative statements; declaration statements; assembler directives

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### A simple assembly scheme

ID: `2301202/u1/assemblers/simple-assembly-scheme`

**Original syllabus:** A Simple Assembly Scheme

How an assembler translates statements using symbol and opcode tables.

**Scope:** How an assembler translates statements using symbol and opcode tables.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** simple assembly scheme

**Reference points:** symbol table; mnemonic opcode table; location counter

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Pass structure of assemblers

ID: `2301202/u1/assemblers/pass-structure`

**Original syllabus:** Pass Structure of Assemblers

Why assemblers use one or two passes, and forward references.

**Scope:** Why assemblers use one or two passes, and forward references.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** pass structure

**Reference points:** forward reference; one pass vs two pass

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Design of two pass assembler

ID: `2301202/u1/assemblers/two-pass-assembler`

**Original syllabus:** Design of Two Pass Assembler

Pass I builds the symbol table and intermediate code; pass II generates target code.

**Scope:** Separate symbol/address collection from final translation across two passes.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** two pass assembler, two-pass assembler

**Reference points:** pass i; pass ii; intermediate code; symtab; littab; pooltab

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Single pass assembler:** Single pass assembler: Translate in one pass, handling forward references through an appropriate scheme. Design of two pass assembler: Separate symbol/address collection from final translation across two passes. Shared family membership alone does not establish assessed overlap.

### Single pass assembler

ID: `2301202/u1/assemblers/single-pass-assembler`

**Original syllabus:** Single pass Assembler

Assembling in one pass by backpatching forward references.

**Scope:** Translate in one pass, handling forward references through an appropriate scheme.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** single pass assembler, one pass assembler

**Reference points:** backpatching; table of incomplete instructions

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Design of two pass assembler:** Single pass assembler: Translate in one pass, handling forward references through an appropriate scheme. Design of two pass assembler: Separate symbol/address collection from final translation across two passes. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Confirm the prescribed forward-reference handling scheme and terminology; supporting implementation details are not universal requirements.

## Process management

ID: `2301202/u2`

**Original syllabus:** Unit II Process management (08 hrs) CO2

Hours: 8; outcomes: CO2.

### Introduction to operating systems

ID: `2301202/u2/introduction-to-os`

**Original syllabus:** Introduction to Operating Systems

What an operating system is, its goals and services.

**Scope:** What an operating system is, its goals and services.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** introduction to operating systems, what is an operating system, functions of os

**Reference points:** os services; system calls; kernel

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Types of operating systems

ID: `2301202/u2/types-of-os`

**Original syllabus:** Types of operating systems:

Batch, time-sharing, network, distributed and real-time operating systems.

**Scope:** Batch, time-sharing, network, distributed and real-time operating systems.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** types of operating systems, types of os

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Batch operating system

ID: `2301202/u2/types-of-os/batch`

**Original syllabus:** Batch

Jobs grouped and run without user interaction.

**Scope:** Execute submitted jobs without ongoing interactive use.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** batch os, batch processing system

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Time-sharing operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Time-sharing operating system: Share execution time to support interactive use. Shared family membership alone does not establish assessed overlap.
- **Compared with Network operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Network operating system: Provide network services while machines retain their identities. Shared family membership alone does not establish assessed overlap.
- **Compared with Distributed operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Real-time operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.

### Time-sharing operating system

ID: `2301202/u2/types-of-os/time-sharing`

**Original syllabus:** Time-sharing

Many users share the CPU through rapid switching.

**Scope:** Share execution time to support interactive use.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** time-sharing OS, time sharing operating system

**Related terms, not aliases:** [{"term": "multitasking OS", "relation": "overlapping_but_not_identical"}]

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Batch operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Time-sharing operating system: Share execution time to support interactive use. Shared family membership alone does not establish assessed overlap.
- **Compared with Network operating system:** Time-sharing operating system: Share execution time to support interactive use. Network operating system: Provide network services while machines retain their identities. Shared family membership alone does not establish assessed overlap.
- **Compared with Distributed operating system:** Time-sharing operating system: Share execution time to support interactive use. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Real-time operating system:** Time-sharing operating system: Share execution time to support interactive use. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.

### Network operating system

ID: `2301202/u2/types-of-os/network`

**Original syllabus:** Network

OS that provides services to computers over a network.

**Scope:** Provide network services while machines retain their identities.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** network os, network operating system

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Batch operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Network operating system: Provide network services while machines retain their identities. Shared family membership alone does not establish assessed overlap.
- **Compared with Time-sharing operating system:** Time-sharing operating system: Share execution time to support interactive use. Network operating system: Provide network services while machines retain their identities. Shared family membership alone does not establish assessed overlap.
- **Compared with Distributed operating system:** Network operating system: Provide network services while machines retain their identities. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Real-time operating system:** Network operating system: Provide network services while machines retain their identities. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.

### Distributed operating system

ID: `2301202/u2/types-of-os/distributed`

**Original syllabus:** Distributed

One OS managing a collection of networked machines as a single system.

**Scope:** Coordinate machines with an integrated system view.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** distributed os, distributed operating system

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Batch operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Time-sharing operating system:** Time-sharing operating system: Share execution time to support interactive use. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Network operating system:** Network operating system: Provide network services while machines retain their identities. Distributed operating system: Coordinate machines with an integrated system view. Shared family membership alone does not establish assessed overlap.
- **Compared with Real-time operating system:** Distributed operating system: Coordinate machines with an integrated system view. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.

### Real-time operating system

ID: `2301202/u2/types-of-os/real-time`

**Original syllabus:** real-time

Operating systems designed around timing constraints. Hard and soft real-time systems differ in the consequences of missing deadlines. Real-time does not simply mean fast execution.

**Scope:** Meet specified timing constraints; distinguish hard and soft deadlines.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** real time os, real-time operating system

**Reference points:** hard real time; soft real time

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Batch operating system:** Batch operating system: Execute submitted jobs without ongoing interactive use. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.
- **Compared with Time-sharing operating system:** Time-sharing operating system: Share execution time to support interactive use. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.
- **Compared with Network operating system:** Network operating system: Provide network services while machines retain their identities. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.
- **Compared with Distributed operating system:** Distributed operating system: Coordinate machines with an integrated system view. Real-time operating system: Meet specified timing constraints; distinguish hard and soft deadlines. Shared family membership alone does not establish assessed overlap.

### Process

ID: `2301202/u2/process`

**Original syllabus:** Process:

The process concept, its control block, states and communication.

**Scope:** The process concept, its control block, states and communication.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** None asserted.

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Process concept

ID: `2301202/u2/process/concept`

**Original syllabus:** Concept

A program in execution and its parts in memory.

**Scope:** Explain the executing program and its execution context.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** process concept, what is a process

**Reference points:** program vs process; text data stack heap

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Process control block:** Process concept: Explain the executing program and its execution context. Process control block: Describe the stored process-management record. Shared family membership alone does not establish assessed overlap.
- **Compared with Process state diagram:** Process concept: Explain the executing program and its execution context. Process state diagram: Describe lifecycle states and transitions. Shared family membership alone does not establish assessed overlap.
- **Compared with Inter-process communication:** Process concept: Explain the executing program and its execution context. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.

### Process control block

ID: `2301202/u2/process/pcb`

**Original syllabus:** Process control block

The data structure the OS keeps for each process.

**Scope:** Describe the stored process-management record.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** process control block

**Reference points:** process state; program counter; registers; scheduling information

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Process concept:** Process concept: Explain the executing program and its execution context. Process control block: Describe the stored process-management record. Shared family membership alone does not establish assessed overlap.
- **Compared with Process state diagram:** Process control block: Describe the stored process-management record. Process state diagram: Describe lifecycle states and transitions. Shared family membership alone does not establish assessed overlap.
- **Compared with Inter-process communication:** Process control block: Describe the stored process-management record. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.

### Process state diagram

ID: `2301202/u2/process/state-diagram`

**Original syllabus:** Process state diagram

States a process moves through and the transitions between them.

**Scope:** Describe lifecycle states and transitions.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** process states, process state transition diagram

**Reference points:** new ready running waiting terminated; state transitions

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Process concept:** Process concept: Explain the executing program and its execution context. Process state diagram: Describe lifecycle states and transitions. Shared family membership alone does not establish assessed overlap.
- **Compared with Process control block:** Process control block: Describe the stored process-management record. Process state diagram: Describe lifecycle states and transitions. Shared family membership alone does not establish assessed overlap.
- **Compared with Inter-process communication:** Process state diagram: Describe lifecycle states and transitions. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.

### Inter-process communication

ID: `2301202/u2/process/ipc`

**Original syllabus:** Inter-process communication

Shared memory and message passing between processes.

**Scope:** Describe data exchange through shared memory or messages.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** inter process communication, interprocess communication

**Reference points:** shared memory; message passing; pipes

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Process concept:** Process concept: Explain the executing program and its execution context. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.
- **Compared with Process control block:** Process control block: Describe the stored process-management record. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.
- **Compared with Process state diagram:** Process state diagram: Describe lifecycle states and transitions. Inter-process communication: Describe data exchange through shared memory or messages. Shared family membership alone does not establish assessed overlap.

### Process scheduling types

ID: `2301202/u2/cpu-scheduling`

**Original syllabus:** Process scheduling types:

CPU scheduling algorithms and how to compute waiting and turnaround times.

**Scope:** CPU scheduling algorithms and how to compute waiting and turnaround times.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** cpu scheduling, process scheduling, scheduling algorithms

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant


### First come first serve (CPU scheduling)

ID: `2301202/u2/cpu-scheduling/fcfs`

**Original syllabus:** First come first serve

Processes run in arrival order.

**Scope:** Select ready processes in arrival order.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** first come first serve scheduling, fcfs scheduling, first come first served

**Reference points:** arrival order; convoy effect; non-preemptive

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with Shortest job first:** First come first serve (CPU scheduling): Select ready processes in arrival order. Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Shared family membership alone does not establish assessed overlap.
- **Compared with Round robin:** First come first serve (CPU scheduling): Select ready processes in arrival order. Round robin: Rotate ready processes using a time quantum. Shared family membership alone does not establish assessed overlap.
- **Compared with Priority-based scheduling:** First come first serve (CPU scheduling): Select ready processes in arrival order. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.

### Shortest job first

ID: `2301202/u2/cpu-scheduling/sjf`

**Original syllabus:** Shortest job first

Scheduling based on the shortest CPU burst. Distinguish non-preemptive SJF from shortest-remaining-time-first; preserve arrival times, preemption assumptions and requested performance measures.

**Scope:** Select by CPU burst or remaining burst; keep the preemption variant explicit.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** shortest job first, SJF

**Related terms, not aliases:** [{"term": "shortest remaining time first", "relation": "preemptive_variant", "alias": "SRTF"}]

**Reference points:** shortest burst; srtf; burst length prediction

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Aspect: Non-preemptive SJF.** Select the shortest next burst without interrupting the running process.
- **Aspect: Preemptive shortest-remaining-time variant.** Treat SRTF as a related variant; require explicit question assumptions.
- **Compared with First come first serve (CPU scheduling):** First come first serve (CPU scheduling): Select ready processes in arrival order. Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Shared family membership alone does not establish assessed overlap.
- **Compared with Round robin:** Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Round robin: Rotate ready processes using a time quantum. Shared family membership alone does not establish assessed overlap.
- **Compared with Priority-based scheduling:** Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.
- **Review needed:** Confirm whether in-syllabus SJF questions include SRTF; never assume the variant when a problem is underspecified.

### Round robin

ID: `2301202/u2/cpu-scheduling/round-robin`

**Original syllabus:** Round robin

Each process gets a fixed time quantum in turn.

**Scope:** Rotate ready processes using a time quantum.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** round robin scheduling

**Reference points:** time quantum; preemptive; context switch

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First come first serve (CPU scheduling):** First come first serve (CPU scheduling): Select ready processes in arrival order. Round robin: Rotate ready processes using a time quantum. Shared family membership alone does not establish assessed overlap.
- **Compared with Shortest job first:** Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Round robin: Rotate ready processes using a time quantum. Shared family membership alone does not establish assessed overlap.
- **Compared with Priority-based scheduling:** Round robin: Rotate ready processes using a time quantum. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.

### Priority-based scheduling

ID: `2301202/u2/cpu-scheduling/priority`

**Original syllabus:** Priority-based scheduling

The highest-priority process runs first; starvation and aging.

**Scope:** Select by priority; retain priority ordering and preemption conventions.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** priority scheduling

**Reference points:** priority number; starvation; aging

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First come first serve (CPU scheduling):** First come first serve (CPU scheduling): Select ready processes in arrival order. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.
- **Compared with Shortest job first:** Shortest job first: Select by CPU burst or remaining burst; keep the preemption variant explicit. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.
- **Compared with Round robin:** Round robin: Rotate ready processes using a time quantum. Priority-based scheduling: Select by priority; retain priority ordering and preemption conventions. Shared family membership alone does not establish assessed overlap.

### Threads

ID: `2301202/u2/threads`

**Original syllabus:** Threads:

Threads, multicore programming and threading models.

**Scope:** Threads, multicore programming and threading models.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** None asserted.

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Multi-core programming

ID: `2301202/u2/threads/multicore-programming`

**Original syllabus:** Multi-core programming

Programming for multicore systems: concurrency vs parallelism and its challenges.

**Scope:** Parallel/concurrent work decomposition across cores.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** multicore programming

**Reference points:** concurrency vs parallelism; data parallelism; task parallelism

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Multithreading models:** Multi-core programming: Parallel/concurrent work decomposition across cores. Multithreading models: Mappings between user and kernel threads. Shared family membership alone does not establish assessed overlap.
- **Compared with Implicit threading:** Multi-core programming: Parallel/concurrent work decomposition across cores. Implicit threading: Thread management delegated to runtime/compiler mechanisms. Shared family membership alone does not establish assessed overlap.
- **Compared with Threading issues:** Multi-core programming: Parallel/concurrent work decomposition across cores. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.

### Multithreading models

ID: `2301202/u2/threads/multithreading-models`

**Original syllabus:** Multithreading models

Mapping user threads to kernel threads.

**Scope:** Mappings between user and kernel threads.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** multithreading models, threading models

**Reference points:** many-to-one; one-to-one; many-to-many; user vs kernel threads

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Multi-core programming:** Multi-core programming: Parallel/concurrent work decomposition across cores. Multithreading models: Mappings between user and kernel threads. Shared family membership alone does not establish assessed overlap.
- **Compared with Implicit threading:** Multithreading models: Mappings between user and kernel threads. Implicit threading: Thread management delegated to runtime/compiler mechanisms. Shared family membership alone does not establish assessed overlap.
- **Compared with Threading issues:** Multithreading models: Mappings between user and kernel threads. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.

### Implicit threading

ID: `2301202/u2/threads/implicit-threading`

**Original syllabus:** Implicit threading

Letting compilers and libraries manage threads.

**Scope:** Thread management delegated to runtime/compiler mechanisms.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** implicit threading

**Reference points:** thread pools; openmp; fork-join

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Multi-core programming:** Multi-core programming: Parallel/concurrent work decomposition across cores. Implicit threading: Thread management delegated to runtime/compiler mechanisms. Shared family membership alone does not establish assessed overlap.
- **Compared with Multithreading models:** Multithreading models: Mappings between user and kernel threads. Implicit threading: Thread management delegated to runtime/compiler mechanisms. Shared family membership alone does not establish assessed overlap.
- **Compared with Threading issues:** Implicit threading: Thread management delegated to runtime/compiler mechanisms. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.

### Threading issues

ID: `2301202/u2/threads/threading-issues`

**Original syllabus:** Threading issues

Problems specific to multithreaded programs.

**Scope:** Lifecycle, signals, cancellation and other multithreading concerns.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** threading issues

**Reference points:** fork and exec; signal handling; thread cancellation; thread-local storage

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Multi-core programming:** Multi-core programming: Parallel/concurrent work decomposition across cores. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.
- **Compared with Multithreading models:** Multithreading models: Mappings between user and kernel threads. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.
- **Compared with Implicit threading:** Implicit threading: Thread management delegated to runtime/compiler mechanisms. Threading issues: Lifecycle, signals, cancellation and other multithreading concerns. Shared family membership alone does not establish assessed overlap.

## Process coordination

ID: `2301202/u3`

**Original syllabus:** Unit III Process coordination (07 hrs) CO3

Hours: 7; outcomes: CO3.

### Synchronization

ID: `2301202/u3/synchronization`

**Original syllabus:** Synchronization:

Coordinating processes that share data: the critical-section problem and its solutions.

**Scope:** Coordinating processes that share data: the critical-section problem and its solutions.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** process synchronization

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### The critical-section problem

ID: `2301202/u3/synchronization/critical-section-problem`

**Original syllabus:** The critical-section problem

Ensuring only one process runs its critical section at a time.

**Scope:** Required properties: mutual exclusion, progress and bounded waiting.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** critical section problem, critical section

**Reference points:** mutual exclusion; progress; bounded waiting; race condition

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Peterson's solution:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Shared family membership alone does not establish assessed overlap.
- **Compared with Synchronization hardware:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Synchronization hardware: Atomic primitives used to construct synchronization. Shared family membership alone does not establish assessed overlap.
- **Compared with Mutex locks:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Semaphores:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.

### Peterson's solution

ID: `2301202/u3/synchronization/petersons-solution`

**Original syllabus:** Peterson’s solution

A software solution to the critical-section problem for two processes.

**Scope:** A two-process software protocol under its memory-ordering assumptions.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** peterson's solution, peterson's algorithm

**Reference points:** flag array; turn variable; two processes

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with The critical-section problem:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Shared family membership alone does not establish assessed overlap.
- **Compared with Synchronization hardware:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Synchronization hardware: Atomic primitives used to construct synchronization. Shared family membership alone does not establish assessed overlap.
- **Compared with Mutex locks:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Semaphores:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.

### Synchronization hardware

ID: `2301202/u3/synchronization/synchronization-hardware`

**Original syllabus:** Synchronization hardware

Atomic hardware instructions used to build locks.

**Scope:** Atomic primitives used to construct synchronization.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** hardware synchronization

**Reference points:** test_and_set; compare_and_swap; atomic instruction

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with The critical-section problem:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Synchronization hardware: Atomic primitives used to construct synchronization. Shared family membership alone does not establish assessed overlap.
- **Compared with Peterson's solution:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Synchronization hardware: Atomic primitives used to construct synchronization. Shared family membership alone does not establish assessed overlap.
- **Compared with Mutex locks:** Synchronization hardware: Atomic primitives used to construct synchronization. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Semaphores:** Synchronization hardware: Atomic primitives used to construct synchronization. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.

### Mutex locks

ID: `2301202/u3/synchronization/mutex-locks`

**Original syllabus:** Mutex locks

Mutual-exclusion locks protect critical sections using acquisition and release. Ownership semantics distinguish a mutex from a semaphore; waiting may spin or block depending on the implementation.

**Scope:** Ownership-based mutual exclusion; acquisition and release.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** mutex, mutex lock

**Reference points:** acquire and release; spinlock; busy waiting

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with The critical-section problem:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Peterson's solution:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Synchronization hardware:** Synchronization hardware: Atomic primitives used to construct synchronization. Mutex locks: Ownership-based mutual exclusion; acquisition and release. Shared family membership alone does not establish assessed overlap.
- **Compared with Semaphores:** Mutex locks: Ownership-based mutual exclusion; acquisition and release. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.

### Semaphores

ID: `2301202/u3/synchronization/semaphores`

**Original syllabus:** Semaphores

Integer variables with wait and signal operations; counting and binary semaphores.

**Scope:** Wait/signal synchronization using binary or counting state; not identical to mutex ownership.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** semaphore

**Reference points:** wait and signal; counting semaphore; binary semaphore

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with The critical-section problem:** The critical-section problem: Required properties: mutual exclusion, progress and bounded waiting. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.
- **Compared with Peterson's solution:** Peterson's solution: A two-process software protocol under its memory-ordering assumptions. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.
- **Compared with Synchronization hardware:** Synchronization hardware: Atomic primitives used to construct synchronization. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.
- **Compared with Mutex locks:** Mutex locks: Ownership-based mutual exclusion; acquisition and release. Semaphores: Wait/signal synchronization using binary or counting state; not identical to mutex ownership. Shared family membership alone does not establish assessed overlap.

### Classic problems of synchronization

ID: `2301202/u3/classic-problems`

**Original syllabus:** Classic problems of synchronization:

Standard synchronization problems and their semaphore solutions.

**Scope:** Standard synchronization problems and their semaphore solutions.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** classical problems of synchronization, classic synchronization problems

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Producer-consumer problem

ID: `2301202/u3/classic-problems/producer-consumer`

**Original syllabus:** Producer-consumer problem

A bounded buffer shared by producers and consumers.

**Scope:** Coordinate buffer occupancy and mutually exclusive access.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** producer consumer problem, bounded buffer problem

**Reference points:** bounded buffer; full and empty semaphores

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Readers-writers problem:** Producer-consumer problem: Coordinate buffer occupancy and mutually exclusive access. Readers-writers problem: Allow concurrent readers while controlling writers. Shared family membership alone does not establish assessed overlap.
- **Compared with Dining philosophers problem:** Producer-consumer problem: Coordinate buffer occupancy and mutually exclusive access. Dining philosophers problem: Coordinate competing acquisition of shared resources and avoid deadlock/starvation. Shared family membership alone does not establish assessed overlap.

### Readers-writers problem

ID: `2301202/u3/classic-problems/reader-writer`

**Original syllabus:** Reader/writer problem

Many readers or one writer may access shared data.

**Scope:** Allow concurrent readers while controlling writers.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** reader writer problem, readers writers problem

**Reference points:** readers preference; writers preference; read count

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Producer-consumer problem:** Producer-consumer problem: Coordinate buffer occupancy and mutually exclusive access. Readers-writers problem: Allow concurrent readers while controlling writers. Shared family membership alone does not establish assessed overlap.
- **Compared with Dining philosophers problem:** Readers-writers problem: Allow concurrent readers while controlling writers. Dining philosophers problem: Coordinate competing acquisition of shared resources and avoid deadlock/starvation. Shared family membership alone does not establish assessed overlap.

### Dining philosophers problem

ID: `2301202/u3/classic-problems/dining-philosophers`

**Original syllabus:** Dining philosopher problem

Five philosophers sharing chopsticks; deadlock and starvation.

**Scope:** Coordinate competing acquisition of shared resources and avoid deadlock/starvation.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** dining philosopher problem, dining philosophers

**Reference points:** chopsticks; deadlock-free solution

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Producer-consumer problem:** Producer-consumer problem: Coordinate buffer occupancy and mutually exclusive access. Dining philosophers problem: Coordinate competing acquisition of shared resources and avoid deadlock/starvation. Shared family membership alone does not establish assessed overlap.
- **Compared with Readers-writers problem:** Readers-writers problem: Allow concurrent readers while controlling writers. Dining philosophers problem: Coordinate competing acquisition of shared resources and avoid deadlock/starvation. Shared family membership alone does not establish assessed overlap.

### Deadlock

ID: `2301202/u3/deadlock`

**Original syllabus:** Deadlock:

How deadlocks arise and how the OS prevents, avoids, detects and recovers from them.

**Scope:** How deadlocks arise and how the OS prevents, avoids, detects and recovers from them.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** deadlocks

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Deadlock characterization

ID: `2301202/u3/deadlock/characterization`

**Original syllabus:** Deadlock characterization

The four necessary conditions and the resource-allocation graph.

**Scope:** Conditions and models describing when deadlock can arise.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** necessary conditions for deadlock, deadlock conditions

**Reference points:** mutual exclusion; hold and wait; no preemption; circular wait; resource allocation graph

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Methods for handling deadlocks:** Deadlock characterization: Conditions and models describing when deadlock can arise. Methods for handling deadlocks: Overview comparing available handling strategies. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock prevention:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock avoidance:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock detection:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Recovery from deadlock:** Deadlock characterization: Conditions and models describing when deadlock can arise. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

### Methods for handling deadlocks

ID: `2301202/u3/deadlock/handling-methods`

**Original syllabus:** Methods for handling deadlocks

The overall strategies: prevent, avoid, detect and recover, or ignore.

**Scope:** Overview comparing available handling strategies.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** methods for handling deadlocks, deadlock handling

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Deadlock characterization:** Deadlock characterization: Conditions and models describing when deadlock can arise. Methods for handling deadlocks: Overview comparing available handling strategies. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock prevention:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock avoidance:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock detection:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Recovery from deadlock:** Methods for handling deadlocks: Overview comparing available handling strategies. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

### Deadlock prevention

ID: `2301202/u3/deadlock/prevention`

**Original syllabus:** Deadlock prevention

Making one of the four necessary conditions impossible.

**Scope:** Constrain allocation so a necessary deadlock condition cannot hold.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** deadlock prevention

**Reference points:** deny hold and wait; allow preemption; resource ordering

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Deadlock characterization:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Shared family membership alone does not establish assessed overlap.
- **Compared with Methods for handling deadlocks:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock avoidance:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock detection:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Recovery from deadlock:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

### Deadlock avoidance

ID: `2301202/u3/deadlock/avoidance`

**Original syllabus:** Deadlock avoidance

Granting requests only if the system stays in a safe state.

**Scope:** Evaluate allocation against safety before granting requests.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** deadlock avoidance

**Reference points:** safe state; banker's algorithm; resource request algorithm; safety algorithm

**Tasks to distinguish:** explain, trace, calculate, justify

**Preserve in the question:** resource model; available/allocation/maximum data; safety versus detection task; safe sequence versus request-grant decision; assumptions

- **Compared with Deadlock characterization:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Methods for handling deadlocks:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock prevention:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Deadlock avoidance: Evaluate allocation against safety before granting requests. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock detection:** Deadlock avoidance: Evaluate allocation against safety before granting requests. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Recovery from deadlock:** Deadlock avoidance: Evaluate allocation against safety before granting requests. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

### Deadlock detection

ID: `2301202/u3/deadlock/detection`

**Original syllabus:** detection

Finding deadlocks that have occurred using wait-for graphs or a detection algorithm.

**Scope:** Determine whether deadlock exists after allocations.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** deadlock detection

**Reference points:** wait-for graph; detection algorithm

**Tasks to distinguish:** explain, trace, calculate, justify

**Preserve in the question:** resource model; available/allocation/maximum data; safety versus detection task; safe sequence versus request-grant decision; assumptions

- **Compared with Deadlock characterization:** Deadlock characterization: Conditions and models describing when deadlock can arise. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Methods for handling deadlocks:** Methods for handling deadlocks: Overview comparing available handling strategies. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock prevention:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock avoidance:** Deadlock avoidance: Evaluate allocation against safety before granting requests. Deadlock detection: Determine whether deadlock exists after allocations. Shared family membership alone does not establish assessed overlap.
- **Compared with Recovery from deadlock:** Deadlock detection: Determine whether deadlock exists after allocations. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

### Recovery from deadlock

ID: `2301202/u3/deadlock/recovery`

**Original syllabus:** Recovery from deadlock

Breaking a deadlock by terminating processes or preempting resources.

**Scope:** Resolve an existing deadlock through termination or resource recovery.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** recovery from deadlock, deadlock recovery

**Reference points:** process termination; resource preemption; victim selection; rollback

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Deadlock characterization:** Deadlock characterization: Conditions and models describing when deadlock can arise. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.
- **Compared with Methods for handling deadlocks:** Methods for handling deadlocks: Overview comparing available handling strategies. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock prevention:** Deadlock prevention: Constrain allocation so a necessary deadlock condition cannot hold. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock avoidance:** Deadlock avoidance: Evaluate allocation against safety before granting requests. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.
- **Compared with Deadlock detection:** Deadlock detection: Determine whether deadlock exists after allocations. Recovery from deadlock: Resolve an existing deadlock through termination or resource recovery. Shared family membership alone does not establish assessed overlap.

## Memory Management

ID: `2301202/u4`

**Original syllabus:** Unit IV Memory Management (07 hrs) CO4

Hours: 7; outcomes: CO4.

### Memory partitioning

ID: `2301202/u4/partitioning`

**Original syllabus:** Memory Partitioning:

Dividing main memory into partitions for processes.

**Scope:** Dividing main memory into partitions for processes.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** memory partitioning

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Fixed partitioning

ID: `2301202/u4/partitioning/fixed`

**Original syllabus:** Fixed partitioning

Memory divided into fixed-size partitions; internal fragmentation.

**Scope:** Partitions established in advance; assess internal fragmentation where relevant.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** fixed partitioning, static partitioning

**Reference points:** internal fragmentation; equal and unequal partitions

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Dynamic partitioning:** Fixed partitioning: Partitions established in advance; assess internal fragmentation where relevant. Dynamic partitioning: Partitions sized dynamically; assess external fragmentation and compaction where relevant. Shared family membership alone does not establish assessed overlap.

### Dynamic partitioning

ID: `2301202/u4/partitioning/dynamic`

**Original syllabus:** Dynamic partitioning

Partitions created to fit each process; external fragmentation and compaction.

**Scope:** Partitions sized dynamically; assess external fragmentation and compaction where relevant.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** dynamic partitioning, variable partitioning

**Reference points:** external fragmentation; compaction

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Fixed partitioning:** Fixed partitioning: Partitions established in advance; assess internal fragmentation where relevant. Dynamic partitioning: Partitions sized dynamically; assess external fragmentation and compaction where relevant. Shared family membership alone does not establish assessed overlap.

### Contiguous memory allocation techniques

ID: `2301202/u4/allocation`

**Original syllabus:** Contiguous Memory allocation techniques:

Placement algorithms for contiguous allocation, plus swapping, paging structures and segmentation as printed.

**Scope:** Placement algorithms for contiguous allocation, plus swapping, paging structures and segmentation as printed.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** contiguous memory allocation, memory allocation techniques

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Review needed:** The printed hierarchy groups paging and segmentation under contiguous allocation. Preserve it as a source outline, not an is-a taxonomy.

### First fit

ID: `2301202/u4/allocation/first-fit`

**Original syllabus:** First fit

Allocate the first hole large enough.

**Scope:** Choose the first sufficiently large available hole.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** first fit algorithm

**Reference points:** first hole

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with Best fit:** First fit: Choose the first sufficiently large available hole. Best fit: Choose the smallest sufficiently large available hole. Shared family membership alone does not establish assessed overlap.
- **Compared with Worst fit:** First fit: Choose the first sufficiently large available hole. Worst fit: Choose the largest available hole. Shared family membership alone does not establish assessed overlap.

### Best fit

ID: `2301202/u4/allocation/best-fit`

**Original syllabus:** Best fit

Allocate the smallest hole large enough.

**Scope:** Choose the smallest sufficiently large available hole.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** best fit algorithm

**Reference points:** smallest adequate hole

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First fit:** First fit: Choose the first sufficiently large available hole. Best fit: Choose the smallest sufficiently large available hole. Shared family membership alone does not establish assessed overlap.
- **Compared with Worst fit:** Best fit: Choose the smallest sufficiently large available hole. Worst fit: Choose the largest available hole. Shared family membership alone does not establish assessed overlap.

### Worst fit

ID: `2301202/u4/allocation/worst-fit`

**Original syllabus:** Worst fit

Allocate the largest hole.

**Scope:** Choose the largest available hole.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** worst fit algorithm

**Reference points:** largest hole

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First fit:** First fit: Choose the first sufficiently large available hole. Worst fit: Choose the largest available hole. Shared family membership alone does not establish assessed overlap.
- **Compared with Best fit:** Best fit: Choose the smallest sufficiently large available hole. Worst fit: Choose the largest available hole. Shared family membership alone does not establish assessed overlap.

### Swapping

ID: `2301202/u4/allocation/swapping`

**Original syllabus:** Swapping

Moving processes between main memory and a backing store.

**Scope:** Move a process memory image between memory and backing storage in the specified model.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** swapping

**Reference points:** backing store; roll out roll in

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Structure of the page table:** Swapping: Move a process memory image between memory and backing storage in the specified model. Structure of the page table: Represent mappings from virtual pages to physical frames. Shared family membership alone does not establish assessed overlap.
- **Compared with Segmentation:** Swapping: Move a process memory image between memory and backing storage in the specified model. Segmentation: Represent variable-size logical segments with address and protection metadata. Shared family membership alone does not establish assessed overlap.
- **Compared with Demand paging:** Swapping: Move a process memory image between memory and backing storage in the specified model. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Translation lookaside buffer:** Swapping: Move a process memory image between memory and backing storage in the specified model. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.

### Structure of the page table

ID: `2301202/u4/allocation/page-table-structure`

**Original syllabus:** Structure of the page table

Paging and how page tables are organised.

**Scope:** Represent mappings from virtual pages to physical frames.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** page-table structure, structure of page tables

**Related terms, not aliases:** [{"term": "paging", "relation": "broader_concept"}]

**Reference points:** hierarchical paging; hashed page table; inverted page table; page and frame

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Swapping:** Swapping: Move a process memory image between memory and backing storage in the specified model. Structure of the page table: Represent mappings from virtual pages to physical frames. Shared family membership alone does not establish assessed overlap.
- **Compared with Segmentation:** Structure of the page table: Represent mappings from virtual pages to physical frames. Segmentation: Represent variable-size logical segments with address and protection metadata. Shared family membership alone does not establish assessed overlap.
- **Compared with Demand paging:** Structure of the page table: Represent mappings from virtual pages to physical frames. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Translation lookaside buffer:** Structure of the page table: Represent mappings from virtual pages to physical frames. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.

### Segmentation

ID: `2301202/u4/allocation/segmentation`

**Original syllabus:** Segmentation

Memory divided into variable-length logical segments with a segment table.

**Scope:** Represent variable-size logical segments with address and protection metadata.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** segmentation

**Reference points:** segment table; base and limit; logical view

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Swapping:** Swapping: Move a process memory image between memory and backing storage in the specified model. Segmentation: Represent variable-size logical segments with address and protection metadata. Shared family membership alone does not establish assessed overlap.
- **Compared with Structure of the page table:** Structure of the page table: Represent mappings from virtual pages to physical frames. Segmentation: Represent variable-size logical segments with address and protection metadata. Shared family membership alone does not establish assessed overlap.
- **Compared with Demand paging:** Segmentation: Represent variable-size logical segments with address and protection metadata. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Translation lookaside buffer:** Segmentation: Represent variable-size logical segments with address and protection metadata. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.

### Demand paging

ID: `2301202/u4/allocation/demand-paging`

**Original syllabus:** Demand paging

Loading pages only when needed; page faults and their handling.

**Scope:** Bring a page into memory on demand and handle page faults.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** demand paging

**Related terms, not aliases:** [{"term": "virtual memory", "relation": "broader_concept"}]

**Reference points:** page fault; lazy swapper; valid-invalid bit

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Swapping:** Swapping: Move a process memory image between memory and backing storage in the specified model. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Structure of the page table:** Structure of the page table: Represent mappings from virtual pages to physical frames. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Segmentation:** Segmentation: Represent variable-size logical segments with address and protection metadata. Demand paging: Bring a page into memory on demand and handle page faults. Shared family membership alone does not establish assessed overlap.
- **Compared with Translation lookaside buffer:** Demand paging: Bring a page into memory on demand and handle page faults. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.

### Page replacement algorithms

ID: `2301202/u4/page-replacement`

**Original syllabus:** Page Replacement algorithms:

Choosing which page to evict on a page fault; counting page faults for a reference string.

**Scope:** Choosing which page to evict on a page fault; counting page faults for a reference string.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** page replacement algorithms, page replacement

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### First in first out page replacement

ID: `2301202/u4/page-replacement/fifo`

**Original syllabus:** First in first out

Evict the page that entered memory first.

**Scope:** Evict the page loaded earliest.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** fifo page replacement, first in first out

**Reference points:** oldest page; belady's anomaly

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with Optimal page replacement:** First in first out page replacement: Evict the page loaded earliest. Optimal page replacement: Evict the page whose next use is furthest in the future. Shared family membership alone does not establish assessed overlap.
- **Compared with Least recently used:** First in first out page replacement: Evict the page loaded earliest. Least recently used: Evict the page least recently accessed. Shared family membership alone does not establish assessed overlap.

### Optimal page replacement

ID: `2301202/u4/page-replacement/optimal`

**Original syllabus:** Optimal page replacement

Evict the page not needed for the longest time; the theoretical best.

**Scope:** Evict the page whose next use is furthest in the future.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** optimal page replacement, opt

**Reference points:** furthest future use; lowest page faults

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First in first out page replacement:** First in first out page replacement: Evict the page loaded earliest. Optimal page replacement: Evict the page whose next use is furthest in the future. Shared family membership alone does not establish assessed overlap.
- **Compared with Least recently used:** Optimal page replacement: Evict the page whose next use is furthest in the future. Least recently used: Evict the page least recently accessed. Shared family membership alone does not establish assessed overlap.

### Least recently used

ID: `2301202/u4/page-replacement/lru`

**Original syllabus:** Least recently used

Evict the page unused for the longest time.

**Scope:** Evict the page least recently accessed.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** least recently used, lru page replacement

**Reference points:** recency; counter or stack implementation

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First in first out page replacement:** First in first out page replacement: Evict the page loaded earliest. Least recently used: Evict the page least recently accessed. Shared family membership alone does not establish assessed overlap.
- **Compared with Optimal page replacement:** Optimal page replacement: Evict the page whose next use is furthest in the future. Least recently used: Evict the page least recently accessed. Shared family membership alone does not establish assessed overlap.

### Translation lookaside buffer

ID: `2301202/u4/page-replacement/tlb`

**Original syllabus:** translation lookaside buffer

A cache of recent page-table entries that speeds address translation.

**Scope:** Cache address translations; not a page-eviction policy.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** translation lookaside buffer

**Reference points:** tlb hit and miss; effective access time

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Swapping:** Swapping: Move a process memory image between memory and backing storage in the specified model. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.
- **Compared with Structure of the page table:** Structure of the page table: Represent mappings from virtual pages to physical frames. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.
- **Compared with Segmentation:** Segmentation: Represent variable-size logical segments with address and protection metadata. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.
- **Compared with Demand paging:** Demand paging: Bring a page into memory on demand and handle page faults. Translation lookaside buffer: Cache address translations; not a page-eviction policy. Shared family membership alone does not establish assessed overlap.
- **Review needed:** TLB appears in the printed page-replacement list; it is an address-translation cache, not a replacement algorithm.

## I/O management and Introduction to Linux

ID: `2301202/u5`

**Original syllabus:** Unit V I/O management and Introduction to Linux 07 hrs CO5,CO6

Hours: 7; outcomes: CO5, CO6.

### I/O devices

ID: `2301202/u5/io-devices`

**Original syllabus:** I/O devices

Kinds of I/O devices and how the OS manages them.

**Scope:** Kinds of I/O devices and how the OS manages them.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** i/o devices, io devices, input output devices

**Reference points:** block and character devices; device controllers; dma

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Disk scheduling algorithms

ID: `2301202/u5/disk-scheduling`

**Original syllabus:** Disk scheduling algorithms:

Ordering disk requests to reduce head movement; computing total seek distance.

**Scope:** Ordering disk requests to reduce head movement; computing total seek distance.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** disk scheduling, disk scheduling algorithms

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant


### First come first serve (disk scheduling)

ID: `2301202/u5/disk-scheduling/fcfs`

**Original syllabus:** First come first serve

Serve disk requests in arrival order.

**Scope:** Service disk requests in arrival order.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** fcfs disk scheduling

**Reference points:** arrival order of requests

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with Shortest seek time first:** First come first serve (disk scheduling): Service disk requests in arrival order. Shortest seek time first: Select the request nearest the current head position. Shared family membership alone does not establish assessed overlap.
- **Compared with SCAN:** First come first serve (disk scheduling): Service disk requests in arrival order. SCAN: Sweep in a direction and reverse at the specified endpoint. Shared family membership alone does not establish assessed overlap.
- **Compared with Circular SCAN:** First come first serve (disk scheduling): Service disk requests in arrival order. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.

### Shortest seek time first

ID: `2301202/u5/disk-scheduling/sstf`

**Original syllabus:** Shortest seek time first algorithm

Serve the request closest to the current head position.

**Scope:** Select the request nearest the current head position.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** shortest seek time first

**Reference points:** closest request; starvation

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First come first serve (disk scheduling):** First come first serve (disk scheduling): Service disk requests in arrival order. Shortest seek time first: Select the request nearest the current head position. Shared family membership alone does not establish assessed overlap.
- **Compared with SCAN:** Shortest seek time first: Select the request nearest the current head position. SCAN: Sweep in a direction and reverse at the specified endpoint. Shared family membership alone does not establish assessed overlap.
- **Compared with Circular SCAN:** Shortest seek time first: Select the request nearest the current head position. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.

### SCAN

ID: `2301202/u5/disk-scheduling/scan`

**Original syllabus:** SCAN

The head sweeps to one end servicing requests, then reverses (elevator).

**Scope:** Sweep in a direction and reverse at the specified endpoint.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** scan algorithm, elevator algorithm

**Reference points:** elevator algorithm; direction of head

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First come first serve (disk scheduling):** First come first serve (disk scheduling): Service disk requests in arrival order. SCAN: Sweep in a direction and reverse at the specified endpoint. Shared family membership alone does not establish assessed overlap.
- **Compared with Shortest seek time first:** Shortest seek time first: Select the request nearest the current head position. SCAN: Sweep in a direction and reverse at the specified endpoint. Shared family membership alone does not establish assessed overlap.
- **Compared with Circular SCAN:** SCAN: Sweep in a direction and reverse at the specified endpoint. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.

### Circular SCAN

ID: `2301202/u5/disk-scheduling/c-scan`

**Original syllabus:** Circular-SCAN

Like SCAN but returns to the start without servicing on the return.

**Scope:** Service in one direction and return without servicing; retain return-distance convention.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** c-scan, circular scan

**Reference points:** circular return; uniform wait time

**Tasks to distinguish:** explain, trace, calculate, compare

**Preserve in the question:** algorithm and variant; input sequence/table; initial state; tie-breaking rule; requested measures; intermediate steps versus final result; endpoint/counting conventions where relevant

- **Compared with First come first serve (disk scheduling):** First come first serve (disk scheduling): Service disk requests in arrival order. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.
- **Compared with Shortest seek time first:** Shortest seek time first: Select the request nearest the current head position. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.
- **Compared with SCAN:** SCAN: Sweep in a direction and reverse at the specified endpoint. Circular SCAN: Service in one direction and return without servicing; retain return-distance convention. Shared family membership alone does not establish assessed overlap.

### Bash shell scripting

ID: `2301202/u5/bash`

**Original syllabus:** Bash shell scripting:

Writing shell scripts in bash.

**Scope:** Writing shell scripts in bash.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** shell scripting, bash scripting

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Basic shell commands

ID: `2301202/u5/bash/basic-commands`

**Original syllabus:** Basic shell commands

Everyday commands used at the bash prompt and in scripts.

**Scope:** Everyday commands used at the bash prompt and in scripts.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** basic shell commands, bash commands

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Linux shell commands:** These syllabus entries can cover the same commands. Distinguish only if the question requires different commands, script composition or outputs; location in the syllabus does not prove different content.
- **Compared with Shell scripting language:** Command invocation differs from composing control flow, variables and pipelines into a script. A script can contain a command without being equivalent to a command-definition question.

### Shell scripting language

ID: `2301202/u5/bash/scripting-language`

**Original syllabus:** scripting language

Variables, conditionals, loops and functions in shell scripts.

**Scope:** Variables, conditionals, loops and functions in shell scripts.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** shell script, shell programming, bash script

**Reference points:** variables; if and case; for and while loops; command line arguments

**Tasks to distinguish:** explain, write_code, trace, debug, design

**Preserve in the question:** language and library; hardware/interface; required behavior; input and output; timing and thresholds; implementation versus explanation

- **Compared with Basic shell commands:** Command invocation differs from composing control flow, variables and pipelines into a script. A script can contain a command without being equivalent to a command-definition question.

### Introduction to Linux

ID: `2301202/u5/linux`

**Original syllabus:** Introduction to Linux:

Linux features, file system, commands, utilities and permissions.

**Scope:** Linux features, file system, commands, utilities and permissions.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.; A question on one child is not equivalent to an overview or all-child question.

**Aliases:** linux

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Essential features of Linux

ID: `2301202/u5/linux/features`

**Original syllabus:** Essential features

Key features of Linux as an operating system.

**Scope:** Key features of Linux as an operating system.

**Boundary:** Automatic inclusion of all parent, sibling or child requirements.

**Aliases:** features of linux, linux features

**Reference points:** multiuser; multitasking; portability; open source

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth


### Linux file systems

ID: `2301202/u5/linux/file-systems`

**Original syllabus:** File systems

The Linux file system hierarchy and file types.

**Scope:** Filesystem organization, file types and hierarchy.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** linux file system, file system structure

**Reference points:** root directory; inode; file types

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Directories:** Linux file systems: Filesystem organization, file types and hierarchy. Directories: Directory organization and navigation. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux shell commands:** Linux file systems: Filesystem organization, file types and hierarchy. Linux shell commands: Commands for navigation and file operations. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux utilities:** Linux file systems: Filesystem organization, file types and hierarchy. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with File access rights:** Linux file systems: Filesystem organization, file types and hierarchy. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.

### Directories

ID: `2301202/u5/linux/directories`

**Original syllabus:** directories

Directory structure and working with directories.

**Scope:** Directory organization and navigation.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** linux directories, directory structure

**Reference points:** /home /etc /bin; absolute and relative path

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Linux file systems:** Linux file systems: Filesystem organization, file types and hierarchy. Directories: Directory organization and navigation. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux shell commands:** Directories: Directory organization and navigation. Linux shell commands: Commands for navigation and file operations. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux utilities:** Directories: Directory organization and navigation. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with File access rights:** Directories: Directory organization and navigation. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.

### Linux shell commands

ID: `2301202/u5/linux/shell-commands`

**Original syllabus:** Linux shell commands such as pwd, cd, ls, cat, rm, cp, mkdir

Core commands for navigating and managing files.

**Scope:** Commands for navigation and file operations.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** linux commands, unix commands

**Reference points:** pwd; cd; ls; cat; rm; cp; mkdir

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Linux file systems:** Linux file systems: Filesystem organization, file types and hierarchy. Linux shell commands: Commands for navigation and file operations. Shared family membership alone does not establish assessed overlap.
- **Compared with Directories:** Directories: Directory organization and navigation. Linux shell commands: Commands for navigation and file operations. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux utilities:** Linux shell commands: Commands for navigation and file operations. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with File access rights:** Linux shell commands: Commands for navigation and file operations. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.
- **Compared with Basic shell commands:** These syllabus entries can cover the same commands. Distinguish only if the question requires different commands, script composition or outputs; location in the syllabus does not prove different content.

### Linux utilities

ID: `2301202/u5/linux/utilities`

**Original syllabus:** Linux utilities such as tr, sed, grep, egrep, awk

Text-processing utilities and filters.

**Scope:** Text filtering and processing utilities.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** linux utilities, unix utilities, filters

**Reference points:** tr; sed; grep; egrep; awk

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Linux file systems:** Linux file systems: Filesystem organization, file types and hierarchy. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Directories:** Directories: Directory organization and navigation. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux shell commands:** Linux shell commands: Commands for navigation and file operations. Linux utilities: Text filtering and processing utilities. Shared family membership alone does not establish assessed overlap.
- **Compared with File access rights:** Linux utilities: Text filtering and processing utilities. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.

### File access rights

ID: `2301202/u5/linux/file-access-rights`

**Original syllabus:** File access rights

Read, write and execute permissions for user, group and others.

**Scope:** Permission interpretation and modification.

**Boundary:** The distinct mechanisms or outputs described in the linked same-unit alternatives.

**Aliases:** file permissions, access rights

**Reference points:** rwx; chmod; chown; umask

**Tasks to distinguish:** define, explain, compare, illustrate

**Preserve in the question:** specific concept/aspect; task; requested diagram/example; constraints and negation; required outputs; answer depth

- **Compared with Linux file systems:** Linux file systems: Filesystem organization, file types and hierarchy. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.
- **Compared with Directories:** Directories: Directory organization and navigation. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux shell commands:** Linux shell commands: Commands for navigation and file operations. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.
- **Compared with Linux utilities:** Linux utilities: Text filtering and processing utilities. File access rights: Permission interpretation and modification. Shared family membership alone does not establish assessed overlap.

## Assumptions

- The original tree supplies the official outline; added aspects do not add official syllabus coverage.
- Exact exam question patterns have not been supplied here and are not inferred.
- Prior model-generated textbook details are retained as review material, not independently verified teaching requirements.
- No faculty-feedback learning or automatic ruling propagation is added.
