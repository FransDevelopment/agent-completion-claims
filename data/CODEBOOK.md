# Codebook: `runs.csv`

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

One row per task run, 533 rows, May to October 2026. Rows are in the order the runs were started. The file carries no task text, agent summaries, file names, paths, people, organizations, identifiers or times of day.

## Columns

| Column | Values | Meaning |
|---|---|---|
| `run` | 1 to 533 | Sequence number in start order. Not an identifier in any other system. |
| `date` | `YYYY-MM-DD` | Date the run started (UTC). |
| `runner_kind` | `language_model`, `deterministic`, `workflow` | `language_model`: an AI agent with tool access did the work. `deterministic`: a narrow, rule-bound script. `workflow`: one multi-agent workflow run executed elsewhere, with no recorded model. |
| `model` | `A`, `B`, `C`, `D`, `unknown`, empty | Anonymized model for language-model runs; empty otherwise. See below. |
| `claimed_verdict` | `PASS`, `BLOCKED`, `FAILED`, empty | The verdict in the runner's own completion claim. Empty means the run returned no structured claim. |
| `verifier_decision` | `accepted`, `refused`, empty | The independent verifier's decision on the claim. Empty when there was no claim to check. For a BLOCKED or FAILED claim, `refused` means the task was kept open, which is the expected outcome; `accepted` means the verifier accepted the report as a valid end state. |
| `refusal_reason` | see below, empty | The verifier's recorded reason for a refusal. Empty when the claim was accepted or there was no claim. |
| `goal_asserted` | `yes`, `no`, `missing`, empty | What the claim said about whether the task goal was completed. `missing` means the claim did not say. Deterministic runners usually leave it out. |
| `items_listed` | integer, empty | How many items the claim listed as what it produced. |
| `file_items_listed` | integer, empty | How many of those items were file locations. The rest were other things, such as references to messages. |
| `checks_reported` | integer, empty | How many checks the claim said the runner ran. |

## Models

| Label | Description |
|---|---|
| A | a small model |
| B | a larger model |
| C | a small model |
| D | a larger model |
| `unknown` | one run whose model was not recorded |

Models are anonymized on purpose. The data is observational and confounded by task, date and verifier rules, so it should not be read as a model ranking.

## Refusal reasons

When the verifier recorded more than one reason, the first that applies in this list is used, except that `non_pass_verdict` appears only when no other reason was recorded: 16 language-model BLOCKED claims in late May carry `deliverable_missing`.

| `refusal_reason` | Meaning |
|---|---|
| `non_pass_verdict` | The claim's verdict was BLOCKED or FAILED, so the task stays open. |
| `deliverable_missing` | A document declared by the kind of task was not among the items the claim listed. For the 68 refused language-model PASS claims with this reason, a check of the underlying records also found no such file at the declared location. |
| `no_checks` | A language-model runner claimed PASS but reported no checks. |
| `goal_not_asserted` | A language-model runner claimed PASS but did not assert that the goal was completed. In both refusals with this reason, the claim said the goal was not completed. |
| `runner_not_permitted` | A deterministic runner claimed PASS on a kind of request it is not permitted to complete. |

## Refusal groups

REPORT.md groups refused language-model PASS claims by `refusal_reason`: A is `deliverable_missing`, B is `no_checks`, C is `goal_not_asserted`. Group A is split further by what the claim listed: only file locations, at least one item that is not a file location, or nothing (`items_listed` is 0). `analysis/reproduce.py --check` requires that no refused language-model PASS claim has any other reason.

## What the verifier checked

From the start of May 2026 the verifier checked that a PASS report was complete and that any documents declared by the kind of task were present as non-empty files. It judged structure and delivery, not quality. The `date` column shows when each kind of refusal first appears: `no_checks` on 8 May, when agents were first required to report their checks; `deliverable_missing` on 13 May, after the instructions given to the agents changed between runs 140 and 141 (see REPORT.md); `goal_not_asserted` on 17 May.
