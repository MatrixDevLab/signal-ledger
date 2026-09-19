#!/usr/bin/env python3
"""Measure a transparent prose cue against paraphrase and quote controls."""
import json
import re
import sys
from pathlib import Path


CASES = [
    {"id": "explicit_because", "expected_inference": True, "text": "The result changed because the source was stale."},
    {"id": "explicit_therefore", "expected_inference": True, "text": "The source is stale; therefore the claim needs review."},
    {"id": "explicit_demonstrates", "expected_inference": True, "text": "The replay demonstrates that the missing field changed the decision."},
    {"id": "paraphrase_given", "expected_inference": True, "text": "Given the mismatch, the record supports a review request."},
    {"id": "paraphrase_follows", "expected_inference": True, "text": "The review request follows from the missing evidence."},
    {"id": "paraphrase_points", "expected_inference": True, "text": "Taken together, the samples point to a coverage gap."},
    {"id": "paraphrase_consistent", "expected_inference": True, "text": "The result is consistent with a stale handoff."},
    {"id": "direct_return", "expected_inference": False, "text": "The parser returned eight records and zero errors."},
    {"id": "direct_timestamp", "expected_inference": False, "text": "The source was opened at 12:00 and its qualifier was retained."},
    {"id": "reported_count", "expected_inference": False, "text": "The run reported four warnings in the output."},
    {"id": "quoted_because", "expected_inference": False, "text": "The source contains the sentence: \"It changed because the input was stale.\""},
    {"id": "quoted_therefore", "expected_inference": False, "text": "The report quotes: \"Therefore, the claim needs review.\""},
    {"id": "reported_demonstrates", "expected_inference": False, "text": "The abstract says the experiment demonstrates a coverage gap."},
    {"id": "reported_proves", "expected_inference": False, "text": "The author claims the result proves the policy is safe."},
]

CUES = ("because", "therefore", "thus", "so", "means", "prove", "establish", "confirm", "demonstrate")


def flagged(text):
    lowered = text.lower()
    return any(re.search(rf"\b{re.escape(cue)}s?\b", lowered) for cue in CUES)


def main(output_path):
    rows = []
    for case in CASES:
        hit = flagged(case["text"])
        if case["expected_inference"] and hit:
            classification = "true_positive"
        elif case["expected_inference"]:
            classification = "false_negative"
        elif hit:
            classification = "false_positive"
        else:
            classification = "true_negative"
        rows.append({**case, "flagged": hit, "classification": classification})

    summary = {name: sum(row["classification"] == name for row in rows)
               for name in ("true_positive", "true_negative", "false_positive", "false_negative")}
    result = {
        "schema": 1,
        "title": "Expanded prose-inference cue probe",
        "recorded_at": "2026-09-15",
        "status": "exploratory",
        "scope": "A review-only probe; validator semantics are unchanged.",
        "method": {
            "runs": 2,
            "reproducible": True,
            "input": "Fourteen hand-labelled observation strings covering explicit cues, paraphrases, direct observations, and quoted or reported inference.",
            "detector": "Flag an observation when it contains a word-boundary match for because, therefore, thus, so, means, prove(s), establish(es), confirm(s), or demonstrate(s).",
            "interpretation": "Cue matches are review signals, not truth or inference verdicts.",
        },
        "summary": summary,
        "cases": rows,
        "finding": {
            "result": "The transparent cue set catches explicit inference language but misses paraphrases and flags inference language quoted or attributed to a source.",
            "implication": "A lexical cue can prioritize review, but paraphrase misses and quote false positives make it unsuitable as an enforcement predicate without a separate scope and context check.",
            "next_test": "Compare a typed review warning against downstream decisions while preserving quoted-source and silent-paraphrase controls.",
        },
    }
    Path(output_path).write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: prose_inference_probe.py OUTPUT")
    main(sys.argv[1])
