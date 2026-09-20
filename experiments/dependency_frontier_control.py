#!/usr/bin/env python3
"""Small deterministic control for atomic/molecular dependency invalidation."""
from collections import defaultdict, deque
import json
from pathlib import Path


def frontier(case):
    edges = case["edges"]
    outgoing = defaultdict(list)
    for edge in edges:
        outgoing[edge["from"]].append(edge)
    invalid = set(case["tombstones"])
    queue = deque(case["tombstones"])
    while queue:
        node = queue.popleft()
        for edge in outgoing[node]:
            if edge["from"] in invalid or edge["from"] in case["tombstones"]:
                if edge["to"] not in invalid:
                    invalid.add(edge["to"])
                    queue.append(edge["to"])
    opaque = [e["to"] for e in edges if e["kind"] == "opaque" and e["from"] in invalid]
    bounded = sorted(invalid - set(case["tombstones"]) - set(opaque))
    return {
        "case": case["id"],
        "tombstones": sorted(case["tombstones"]),
        "invalidated": sorted(invalid),
        "bounded_frontier": bounded,
        "opaque_frontier": sorted(opaque),
        "requires_bundle_invalidation": bool(opaque),
    }


def admission(result):
    """Map observed invalidation shape to a review-only consumer action."""
    if result["requires_bundle_invalidation"]:
        return {
            "disposition": "review_bundle",
            "revalidation_scope": result["opaque_frontier"],
        }
    return {
        "disposition": "revalidate_bounded",
        "revalidation_scope": result["bounded_frontier"],
    }


def main():
    path = Path(__file__).with_name("dependency-frontier-control.json")
    fixture = json.loads(path.read_text())
    first = [frontier(case) for case in fixture["cases"]]
    second = [frontier(case) for case in fixture["cases"]]
    result = {
        "fixture": fixture["fixture"],
        "cases": first,
        "repeat_identical": first == second,
        "summary": {
            "case_count": len(first),
            "bounded_cases": sum(not x["requires_bundle_invalidation"] for x in first),
            "opaque_cases": sum(x["requires_bundle_invalidation"] for x in first),
        },
        "boundary": "Synthetic graph control only; it does not infer production dependencies or semantic truth.",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
