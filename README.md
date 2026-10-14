# agent-completion-claims

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

When an AI agent reports that a task is done, how often is that true?

This repository holds a short report and an anonymized dataset from five months of running real work through AI agents, May to October 2026. Almost every run ended with the runner's own completion claim, and a separate, rule-based verifier checked each claim's structure and whether the documents the task required had been delivered.

**Headline:** in May 2026, language-model agents claimed success 143 times, and the verifier refused 98 of those claims (69%). Most refusals (68 of 98) followed a change in my own instructions that, by every sign in the records, stopped telling agents which documents a task required. No agent report named the missing requirement; the check for the declared documents caught every one. In six refused claims, the agent reported PASS while its own report said the goal was not completed.

- [**REPORT.md**](REPORT.md): the write-up, with the failure taxonomy, results by model, and limitations.
- [**data/runs.csv**](data/runs.csv): one anonymized row per task run (533 rows).
- [**data/CODEBOOK.md**](data/CODEBOOK.md): column definitions, model labels and refusal-group rules.
- [**analysis/reproduce.py**](analysis/reproduce.py): reproduces every count and percentage in the report.

## Reproduce

Python 3.9 or later, standard library only:

```bash
python3 analysis/reproduce.py --check
```

It prints every table in the report and exits non-zero if any published number does not match the data.

## Scope

This is a single-operator, observational dataset, not a controlled study. Models, tasks and dates are confounded, so the model table describes what happened and does not rank models. See the limitations in [REPORT.md](REPORT.md#limitations).

## License

Code is Apache 2.0; the report, codebook and data are CC BY 4.0. See [LICENSES.md](LICENSES.md).

## Citation

Moore F. *When an agent says "done": 143 completion claims checked by an independent verifier.* October 2026. https://github.com/FransDevelopment/agent-completion-claims. See [CITATION.cff](CITATION.cff).
