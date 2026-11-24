"""Check exact arithmetic and explicit trace rules for synthetic teaching cases."""
import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "fixtures" / "audits.json"


def ratio(num, den):
    return str(Fraction(num, den)) if den else None


def require_counts(*values):
    if any(type(n) is not int or n < 0 for n in values):
        raise ValueError("expected non-negative integer counts")


def forecast_summary(rows):
    if not rows:
        raise ValueError("no forecast records")
    total = sum(row["n"] for row in rows)
    totals = {model: {"right": 0, "squared_error": Fraction(0)} for model in ("a", "b")}
    for row in rows:
        n, y = row["n"], row["observed"]
        require_counts(n, y)
        if not n or y > n:
            raise ValueError("invalid forecast counts")
        for model, tally in totals.items():
            if not isinstance(row[model], str):
                raise ValueError("probabilities must be decimal strings")
            p = Fraction(row[model])
            if not 0 <= p <= 1:
                raise ValueError("probability outside 0–1")
            tally["right"] += y if p >= Fraction(1, 2) else n - y
            tally["squared_error"] += y * (1 - p) ** 2 + (n - y) * p ** 2
    return {"n": total, "models": {
        model: {"correct": t["right"], "brier": str(t["squared_error"] / total)}
        for model, t in totals.items()
    }}


def paired_summary(rows):
    if not rows:
        raise ValueError("no paired records")
    used = set()
    out = {"attempted": len(rows), "base_correct": 0, "variant_correct": 0,
           "base_returned": 0, "variant_returned": 0, "lost": [], "gained": [],
           "variant_timeouts": [], "changed": 0}
    for row in rows:
        key, k, b, v = (row[x] for x in ("id", "known", "base", "variant"))
        if not isinstance(key, str) or not key or key in used:
            raise ValueError("missing or duplicate paired ID")
        used.add(key)
        require_counts(k, *(n for n in (b, v) if n is not None))
        bp, vp = b == k, v == k
        out["base_correct"] += bp
        out["variant_correct"] += vp
        out["base_returned"] += b is not None
        out["variant_returned"] += v is not None
        out["changed"] += b != v
        if bp and not vp:
            out["lost"].append(key)
        if vp and not bp:
            out["gained"].append(key)
        if v is None:
            out["variant_timeouts"].append(key)
    return out


def channel_summary(channels):
    results = {}
    positive = misses = 0
    for key, row in channels.items():
        tp, fn, fp, tn = (row[x] for x in ("tp", "fn", "fp", "tn"))
        require_counts(tp, fn, fp, tn)
        positive += tp + fn
        misses += fn
        results[key] = {
            "fn_rate": ratio(fn, tp + fn),
            "tp_rate": ratio(tp, tp + fn),
            "fp_rate": ratio(fp, fp + tn),
            "precision": ratio(tp, tp + fp),
            "flag_rate": ratio(tp + fp, tp + fn + fp + tn),
        }
    return {"channels": results, "pooled_miss_rate": ratio(misses, positive)}


def trace_disposition(case, proposal="propose_hold"):
    # A synthetic review rule, not a real authorization or proof of no effect.
    trace, current, status, changes = (
        case[k] for k in ("trace", "current", "status", "changes")
    )
    require_counts(changes)
    if (not isinstance(trace, list) or not isinstance(current, str) or not current or
        any(not isinstance(step, list) or len(step) != 2 or
            any(not isinstance(part, str) or not part for part in step) for step in trace)):
        raise ValueError("malformed workflow step or version")
    if status != "open" or changes or any(step[0] not in ("read", proposal) for step in trace):
        return "stop_out_of_scope_effect_or_trace"
    if len(trace) != 2 or [step[0] for step in trace] != ["read", proposal]:
        return "stop_expected_receipt_missing"
    if any(step[1] != current for step in trace):
        return "stop_stale_evidence"
    return "proposal_for_human_review_only"


def checked_rates(rows):
    result = []
    for count, total in rows:
        require_counts(count, total)
        if count > total:
            raise ValueError("count exceeds total")
        result.append(ratio(count, total))
    return result


def audit(data):
    cap = data["capstone"]
    cohorts = cap["cohorts"]
    return {
        "forecasts": forecast_summary(data["forecasts"]),
        "reserve_above": str(Fraction(1, 1 + 4)),
        "pairs": paired_summary(data["pairs"]),
        "burdens": channel_summary(data["channels"]),
        "workflows": {k: trace_disposition(v) for k, v in data["workflows"].items()},
        "capstone_checks": {
            "extractions": paired_summary(cap["extractions"]),
            "misses": checked_rates(cap["misses"]),
            "cohorts": checked_rates(cohorts),
            "pooled_event_rate": ratio(sum(c for c, _ in cohorts), sum(n for _, n in cohorts)),
            "workflow": trace_disposition(cap["workflow"], "propose_report"),
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, nargs="?", default=DEFAULT)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.fixture.read_text(encoding="utf-8"))
        output = audit(data)
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError) as exc:
        print(f"Fixture rejected: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
