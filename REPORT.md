# When an agent says "done": 143 completion claims checked by an independent verifier

Frans Moore, October 2026

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

## Summary

From May to October 2026 I ran part of a small organization's research, engineering and operations work through an automated dispatcher, which handed each task to a runner, either an AI agent or a deterministic script, and recorded the result. This dataset is every run of that automated dispatcher: 533 task runs. It is not all of the organization's agent work. In the underlying records, agents handed 2,197 tasks to one another between April and October 2026, and only about a quarter of them went through the automated dispatcher; of the 1,146 that were completed, 705 were completed by other routes, such as interactive agent sessions, that filed no structured claim. Work done directly in interactive sessions, without a task being handed off, is not counted anywhere. 517 of the 533 automated dispatcher runs ended with the runner's own structured report: a verdict (PASS, BLOCKED or FAILED), a summary, what it produced, and how it checked its work. Before a task run through the automated dispatcher was recorded as complete, a separate, rule-based verifier checked the structure of that report and whether the documents the task required had been delivered.

In May 2026, language-model agents claimed success (PASS) 143 times. **The verifier refused 98 of those claims (69%).** Each refusal was a structural failure of the claim, not a judgment of quality:

- In 68, documents that the kind of task required were missing. All 68 came after a change on 13 May to the instructions given to the agents, which by every sign in the records stopped naming those documents. No agent report named the missing requirement; the check for the declared documents caught every one.
- In 28, the required documents existed, but the agent reported running no checks. All 28 came before the instruction change.
- In 2, the agent's own report said the goal was not completed, under a verdict of PASS. The same contradiction appears in 4 more refused claims.

The most important result is not a failure rate. It is that **agents' reports did not name a broken task specification, and in six cases contradicted themselves; a simple rule-based check of each report caught both.** A report of completion is a claim, not evidence.

This is a small, single-operator, observational dataset, not a controlled study, and the limitations below matter.

## Setup

- **Tasks.** Each task stated its goal. Some kinds of task also declared documents a completed task had to produce.
- **Runners.** *Language-model runners* gave the task to an AI agent with tool access. *Deterministic runners* were scripts that did narrow, rule-bound work, such as writing a routine note. One further run was a multi-agent workflow executed elsewhere, with no recorded model; it is counted with neither group.
- **The claim.** A run's structured report gave a verdict, a summary, whether the goal was completed, what was produced, how it was checked, and anything that blocked it.
- **The verifier.** A separate process, sharing none of the agent's reasoning, accepted or refused each claim. A refused claim left the task open.

The verifier was new in May. From the start it checked that a PASS report was complete and that any documents declared by the task were present as non-empty files. Two things changed during May:

| Period | What changed | Language-model PASS claims | Refused |
|---|---|---|---|
| 6 to 7 May | (verifier introduced) | 16 | 0 |
| 8 May to the change | agents must also report the checks they ran | 45 | 28 |
| From the change on 13 May | the instructions given to the agents changed | 82 | 70 |

The instruction change came partway through 13 May, between runs 140 and 141 in the data, and the table splits there. PASS claims whose own report said the goal was not completed appear from 13 May; every one was refused, and the first refused with that as the recorded reason came on 17 May. "Accepted" means only that a claim met the rules in force for it.

The verifier judged each claim's structure and whether the required documents existed. It did not judge their content, which came from the agent's own output, so a report could pass and still be poor work.

## Data

| | Runs |
|---|---|
| All automated dispatcher runs, May to October 2026 | 533 |
| Runner claimed PASS | 318 |
| Runner claimed BLOCKED (could not proceed) | 151 |
| Runner claimed FAILED | 48 |
| No structured claim | 16 |

PASS claims by runner type and period:

| | Accepted | Refused | Refusal rate |
|---|---|---|---|
| Language-model agents, May | 45 | 98 | **69%** |
| Deterministic runners, May | 69 | 0 | 0% |
| Deterministic runners, June to October | 98 | 7 | 7% |

The multi-agent workflow run made one accepted PASS claim, in July. Every language-model PASS claim in the dataset falls in May. After May, language-model runners ran only 5 more tasks, and none of those runs claimed PASS; routine work moved to deterministic runners. **So the drop in refusals after May is not evidence that agents improved. It reflects a change in who was making completion claims.**

## What the refused claims looked like

Each refused language-model claim is grouped by the verifier's recorded reason. Where a claim had several problems, the missing document counts first.

**A. Required documents missing (68 claims, 69%).** Every one of these came after the 13 May change, and the last came on 28 May. Before it, model A made 42 PASS claims and none was missing a required document; after it, all 66 of its PASS claims were. In the underlying records (not in the public data), agents before the change wrote the required documents by name; after it, nothing in the records shows that the new instructions named them. So this group is mainly evidence of a regression in my own instructions, not of agents knowingly misreporting.

What makes it worth reporting is how the agents responded. None of them said the task was under-specified or that it could not tell what "done" meant. Each reported PASS. In 56 cases the agent listed other files as its work product; in 10 the list also included things that are not files, such as references to messages and status notes; in 2 it listed nothing. In the underlying records, about half of the files listed were small notes about the agent's own setup and status, and most of the rest were summaries of the run. In most of these claims the agent described getting oriented as if it were the task. A few listed substantive work under a different name.

Model A's reports did change after the instructions did. Of its 158 runs from the change on, 66 reported PASS, 85 BLOCKED and 7 FAILED, against 10 BLOCKED or FAILED in its 52 earlier runs. In the underlying records, nearly all of those BLOCKED reports cited missing tools or write access. So the reports did signal that something was wrong, but none said what: no report said the required documents were missing or unspecified. Until 28 May, the PASS reports said work was being completed while the work the task needed was not being produced. Checking for the declared documents caught every one.

**B. No checks were reported (28 claims, 29%).** The agent claimed PASS and the required documents existed (in the underlying records, all 28 included them and passed that check), but it reported no checks. I count these as **unverified, not false**: the work may have been fine. They were refused because a completion claim with no account of how the agent knew it was done is a claim a verifier cannot tell apart from a confident guess.

**C. PASS while the agent's own report said the goal was not completed (2 claims).** The top-line verdict was PASS while the agent's own report said the goal was not completed. The same contradiction appears in 6 refused claims in all; in the other 4, documents were also missing, so they are counted in group A. One of these six summaries says why: the agent "found no actionable blocker or writable completion path" with the tools it had. It had correctly discovered that it could not finish, and reported success anyway. This is the clearest misreporting in the data. The honest verdict, BLOCKED, was available, and language-model runners used it 112 times elsewhere in the data.

The 7 deterministic refusals after May came from a runner that reported PASS on a kind of request it was not permitted to complete. That is a bug in my runner, not agent behaviour, and I report it to keep the table honest.

## By model

Four models ran language-model tasks; three of them made PASS claims. I give this as a description, not a ranking.

| Model | Runs | PASS claims | PASS refused | BLOCKED | FAILED | No claim |
|---|---|---|---|---|---|---|
| A, a small model | 210 | 108 | 92 (85%) | 89 | 13 | 0 |
| B, a larger model | 63 | 27 | 4 (15%) | 15 | 21 | 0 |
| C, a small model | 19 | 8 | 2 (25%) | 1 | 6 | 4 |
| D, a larger model | 15 | 0 | 0 | 7 | 8 | 0 |

One further language-model run has no recorded model. The models did different tasks on different dates under different rules, so this table cannot separate model from task. Holding the period fixed helps: from the change on, A had 66 of 66 PASS claims refused, B 2 of 9, and C 2 of 7. B and C ran fewer and often different tasks after the change; in the underlying records, none of C's runs after the change was on a kind of task that declared documents, so its rate is not comparable with A's. D never claimed success, which is consistent either with more honest reporting or with harder tasks; the data cannot say which.

## What I take from it

1. **Self-reports did not name a broken specification.** When the instructions stopped naming what "done" required, model A reported BLOCKED or FAILED in 92 of its 158 later runs, mostly citing missing tools or access. But no report named the missing requirement, and all 66 of its PASS claims lacked the required documents. Reading the reports would have shown that something was wrong, not what; a rule-based check of each claim caught it.
2. **Agents describe activity in the language of completion.** Most group A claims listed notes and summaries of the agent's own orientation as its work product. Read on its own, such a report sounds like a finished task.
3. **The honest alternative was available, and in six cases not used.** Language-model runners reported BLOCKED 112 times and FAILED 48 times, so they could say "I cannot finish". In six refused claims they said PASS while their own report said the goal was not completed. What separates those cases is the question I most want to answer.
4. **A verifier has a cost.** Group B is the false-refusal side: work that existed, refused for missing evidence of how it was checked. A deployer who adds a check like this should first run it without the power to block, and learn its refusal rate on legitimate work.

## Limitations

- **One operator, one organization, one period.** The tasks are mine, mostly operations and coordination rather than software engineering.
- **One route, a minority of the work.** The data covers only tasks run through the automated dispatcher. Of the 1,146 handed-off tasks completed between April and October 2026, 705 were completed by other routes and never reached it (from the underlying records, not the public data). The refusal rates describe claims made through the automated dispatcher, not agent work in general.
- **Observational, not controlled.** Models, tasks, dates, instructions and verifier rules are confounded. The model table is descriptive only.
- **Group A reflects my own instruction regression.** It shows how agents report when the specification is broken; it is not evidence that agents ignore requirements they were given.
- **The verifier checks structure, not truth.** The 45 accepted claims are not a verified-correct set; an accepted claim can still be wrong in substance. These numbers bound structural misreporting only.
- **Small n for three of the four models.**

## What I want to study next

A controlled benchmark of completion faithfulness on agentic tasks:

- tasks with machine-checkable deliverables and a known honest verdict, including tasks that are impossible or under-specified by design;
- the same tasks across several models and scaffolds, under fixed verification rules;
- the failure groups above as a labelled taxonomy, plus measurements of when agents choose BLOCKED, or ask, rather than report a false PASS;
- for each kind of monitor (summary-reading, artifact-checking, model-graded), both how many false claims it catches and how much legitimate work it refuses.

The aim is a measurement that tells a deployer which evidence to require before trusting "done", and what that requirement will cost them.

## Data and reproduction

Every count and percentage above, and the July date of the workflow run, is reproduced from [`data/runs.csv`](data/runs.csv) by [`analysis/reproduce.py`](analysis/reproduce.py); run it with `--check` to assert each one. Statements marked as coming from the underlying records are not in the public data. The CSV has one anonymized row per task run, with no task text, summaries, file names or identifiers. Columns and group definitions are in [`data/CODEBOOK.md`](data/CODEBOOK.md).
