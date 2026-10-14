# SPDX-License-Identifier: Apache-2.0
"""Reproduce every number in README.md and REPORT.md from data/runs.csv.

Standard library only. Run from any directory:

    python3 analysis/reproduce.py           # print every published number
    python3 analysis/reproduce.py --check   # also assert each one
"""
import argparse
import collections
import csv
import pathlib
import sys

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "runs.csv"

# Requirement windows. The checks rule starts on 8 May; the instruction change
# falls between runs 140 and 141, on 13 May, so that boundary is a run number.
CHECKS_RULE_DATE = "2026-05-08"
CHANGE_RUN = 141


def load(path=DATA):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def window(r):
    if int(r["run"]) >= CHANGE_RUN:
        return "w3"
    return "w1" if r["date"] < CHECKS_RULE_DATE else "w2"


def deliverable_group(r):
    """Split deliverable_missing claims by what the claim listed instead."""
    listed, files = int(r["items_listed"]), int(r["file_items_listed"])
    if listed == 0:
        return "nothing"
    return "all_files" if files == listed else "some_non_files"


def metrics(rows):
    """Every published number, by name."""
    m = collections.Counter()
    m["runs"] = len(rows)
    m["runs_with_claim"] = sum(1 for r in rows if r["claimed_verdict"])
    for r in rows:
        verdict = r["claimed_verdict"] or "none"
        kind = r["runner_kind"]
        m[f"claimed_{verdict}"] += 1
        m[f"runs_{kind}"] += 1
        if kind != "language_model":
            if verdict == "PASS":
                m[f"{kind}_pass_month_{r['date'][:7]}"] += 1
                period = "may" if r["date"].startswith("2026-05") else "after_may"
                m[f"{kind}_pass_{period}_{r['verifier_decision']}"] += 1
                if r["verifier_decision"] == "refused":
                    m[f"{kind}_refused_{r['refusal_reason']}"] += 1
            continue
        model = r["model"]
        m[f"lm_{verdict}"] += 1
        m[f"model_{model}_runs"] += 1
        m[f"model_{model}_{verdict}"] += 1
        if model == "A":
            m[f"{'w3' if window(r) == 'w3' else 'before'}_model_A_{verdict}"] += 1
        if not r["date"].startswith("2026-05"):
            m["lm_runs_after_may"] += 1
            m[f"lm_after_may_{verdict}"] += 1
        if verdict != "PASS":
            continue
        decision = r["verifier_decision"]
        m[f"lm_pass_{decision}"] += 1
        m[f"model_{model}_pass_{decision}"] += 1
        m[f"{window(r)}_pass"] += 1
        m[f"{window(r)}_pass_{decision}"] += 1
        period = "w3" if window(r) == "w3" else "before"
        m[f"{period}_model_{model}_pass"] += 1
        m[f"{period}_model_{model}_pass_{decision}"] += 1
        if r["refusal_reason"] == "deliverable_missing":
            m[f"{period}_model_{model}_deliverable_missing"] += 1
        if r["goal_asserted"] == "no":
            m[f"lm_pass_goal_no_{decision}"] += 1
        if decision != "refused":
            continue
        reason = r["refusal_reason"]
        m[f"lm_refused_{reason}"] += 1
        m[f"{window(r)}_refused_{reason}"] += 1
        if reason == "deliverable_missing":
            m[f"lm_deliverable_missing_listed_{deliverable_group(r)}"] += 1
            if r["goal_asserted"] == "no":
                m["lm_deliverable_missing_goal_no"] += 1
    known = {"deliverable_missing", "no_checks", "goal_not_asserted"}
    m["lm_refused_other"] = m["lm_pass_refused"] - sum(m[f"lm_refused_{k}"] for k in known)
    m["lm_deliverable_missing_listed_something"] = (
        m["lm_refused_deliverable_missing"] - m["lm_deliverable_missing_listed_nothing"]
    )
    for period in ("before", "w3"):
        m[f"{period}_model_A_runs"] = sum(
            m[f"{period}_model_A_{v}"] for v in ("PASS", "BLOCKED", "FAILED", "none")
        )
        m[f"{period}_model_A_not_pass"] = m[f"{period}_model_A_BLOCKED"] + m[f"{period}_model_A_FAILED"]
    m["deterministic_pass_after_may_total"] = (
        m["deterministic_pass_after_may_accepted"] + m["deterministic_pass_after_may_refused"]
    )
    return m


# Every count stated in README.md or REPORT.md.
EXPECTED = {
    "runs": 533, "runs_with_claim": 517, "claimed_PASS": 318, "claimed_BLOCKED": 151,
    "claimed_FAILED": 48, "claimed_none": 16,
    "runs_language_model": 308, "runs_deterministic": 224, "runs_workflow": 1,
    "lm_PASS": 143, "lm_pass_accepted": 45, "lm_pass_refused": 98,
    "lm_BLOCKED": 112, "lm_FAILED": 48, "lm_none": 5,
    "lm_runs_after_may": 5, "lm_after_may_PASS": 0,
    "deterministic_pass_may_accepted": 69, "deterministic_pass_may_refused": 0,
    "deterministic_pass_after_may_accepted": 98, "deterministic_pass_after_may_refused": 7,
    "deterministic_refused_runner_not_permitted": 7,
    "workflow_pass_after_may_accepted": 1, "workflow_pass_month_2026-07": 1,
    "lm_refused_deliverable_missing": 68, "lm_refused_no_checks": 28,
    "lm_refused_goal_not_asserted": 2, "lm_refused_other": 0,
    "lm_deliverable_missing_listed_all_files": 56,
    "lm_deliverable_missing_listed_some_non_files": 10,
    "lm_deliverable_missing_listed_nothing": 2,
    "lm_deliverable_missing_listed_something": 66,
    "lm_pass_goal_no_refused": 6, "lm_pass_goal_no_accepted": 0,
    "lm_deliverable_missing_goal_no": 4,
    "w1_pass": 16, "w1_pass_refused": 0, "w2_pass": 45, "w2_pass_refused": 28,
    "w2_refused_no_checks": 28, "w3_pass": 82, "w3_pass_refused": 70,
    "w1_refused_deliverable_missing": 0, "w2_refused_deliverable_missing": 0,
    "w3_refused_deliverable_missing": 68, "w3_refused_no_checks": 0,
    "w3_refused_goal_not_asserted": 2,
    "w3_model_A_runs": 158, "w3_model_A_PASS": 66, "w3_model_A_BLOCKED": 85,
    "w3_model_A_FAILED": 7, "w3_model_A_not_pass": 92,
    "before_model_A_pass": 42, "before_model_A_deliverable_missing": 0,
    "before_model_A_runs": 52, "before_model_A_not_pass": 10,
    "w3_model_A_deliverable_missing": 66,
    "model_A_runs": 210, "model_A_PASS": 108, "model_A_pass_refused": 92,
    "model_A_BLOCKED": 89, "model_A_FAILED": 13, "model_A_none": 0,
    "model_B_runs": 63, "model_B_PASS": 27, "model_B_pass_refused": 4,
    "model_B_BLOCKED": 15, "model_B_FAILED": 21, "model_B_none": 0,
    "model_C_runs": 19, "model_C_PASS": 8, "model_C_pass_refused": 2,
    "model_C_BLOCKED": 1, "model_C_FAILED": 6, "model_C_none": 4,
    "model_D_runs": 15, "model_D_PASS": 0, "model_D_pass_refused": 0,
    "model_D_BLOCKED": 7, "model_D_FAILED": 8, "model_D_none": 0,
    "model_unknown_runs": 1, "model_unknown_none": 1,
    "w3_model_A_pass": 66, "w3_model_A_pass_refused": 66,
    "w3_model_B_pass": 9, "w3_model_B_pass_refused": 2,
    "w3_model_C_pass": 7, "w3_model_C_pass_refused": 2,
}

# Every percentage stated, as (numerator, denominator, published whole percent).
PERCENTAGES = [
    ("lm_pass_refused", "lm_PASS", 69),
    ("lm_refused_deliverable_missing", "lm_pass_refused", 69),
    ("lm_refused_no_checks", "lm_pass_refused", 29),
    ("deterministic_pass_after_may_refused", "deterministic_pass_after_may_total", 7),
    ("model_A_pass_refused", "model_A_PASS", 85),
    ("model_B_pass_refused", "model_B_PASS", 15),
    ("model_C_pass_refused", "model_C_PASS", 25),
]


# Every date stated (REPORT.md and data/CODEBOOK.md): when each kind of refusal
# first appears, when a PASS contradicted by its own goal field was first
# refused, and the last refusal for a missing document.
FIRST_SEEN = {
    "no_checks": "2026-05-08", "deliverable_missing": "2026-05-13",
    "goal_not_asserted": "2026-05-17", "goal_not_completed_refused": "2026-05-13",
    "deliverable_missing_last": "2026-05-28",
}


def first_seen(rows):
    seen = {}

    def earliest(key, date):
        if key not in seen or date < seen[key]:
            seen[key] = date

    for r in rows:
        reason = r["refusal_reason"]
        if reason:
            earliest(reason, r["date"])
        contradicted = r["claimed_verdict"] == "PASS" and r["goal_asserted"] == "no"
        if contradicted and r["verifier_decision"] == "refused":
            earliest("goal_not_completed_refused", r["date"])
        if reason == "deliverable_missing" and r["claimed_verdict"] == "PASS":
            seen["deliverable_missing_last"] = max(seen.get("deliverable_missing_last", ""), r["date"])
    return seen


def check(m, seen):
    failures = [f"{k}: expected {v}, got {m[k]}" for k, v in EXPECTED.items() if m[k] != v]
    for num, den, pct in PERCENTAGES:
        got = round(100 * m[num] / m[den]) if m[den] else None
        if got != pct:
            failures.append(f"{num}/{den}: expected {pct}%, got {got}%")
    for reason, date in FIRST_SEEN.items():
        if seen.get(reason) != date:
            failures.append(f"{reason} first seen: expected {date}, got {seen.get(reason)}")
    for line in failures:
        print("MISMATCH", line, file=sys.stderr)
    total = len(EXPECTED) + len(PERCENTAGES) + len(FIRST_SEEN)
    print(f"\ncheck: {total - len(failures)} of {total} published numbers reproduced")
    return not failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="assert every published number")
    parser.add_argument("--data", type=pathlib.Path, default=DATA)
    args = parser.parse_args(argv)
    rows = load(args.data)
    m, seen = metrics(rows), first_seen(rows)
    for key in sorted(m):
        print(f"{key}: {m[key]}")
    for reason in sorted(seen):
        print(f"first seen {reason}: {seen[reason]}")
    if args.check and not check(m, seen):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
