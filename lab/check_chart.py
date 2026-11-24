"""Recalculate comparisons for the chapter's two-site synthetic fixture."""
import argparse
import csv
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

FIELDS = ["site", "before", "after"]


def read_visits(path):
    data = {}
    with path.open(newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source, strict=True)
        if rows.fieldnames != FIELDS:
            raise ValueError("Expected site,before,after header")
        for row in rows:
            if set(row) != set(FIELDS) or any(row[k] is None for k in FIELDS):
                raise ValueError("Each row must have exactly three populated fields")
            name = row["site"]
            if not re.fullmatch(r"[A-Z][a-z]{1,15}", name) or name in data:
                raise ValueError("Expected unique synthetic site labels")
            if any(not re.fullmatch(r"[0-9]{1,6}", row[k]) for k in ("before", "after")):
                raise ValueError("Expected non-negative integer visit counts")
            data[name] = tuple(int(row[k]) for k in ("before", "after"))
    if len(data) != 2:
        raise ValueError("Expected exactly two sites")
    return data


def compare(data):
    comparisons = {}
    for name, (before, after) in data.items():
        change = after - before
        fraction = str(Fraction(change, before)) if before else None
        comparisons[name] = {
            "before_visits": before, "after_visits": after,
            "change_visits": change, "baseline_fraction": fraction,
        }
    changes = [after - before for before, after in data.values()]
    rates = [Fraction(after - before, before) if before else None
             for before, after in data.values()]
    return {
        "sites": comparisons,
        "tie_on_change_visits": changes[0] == changes[1],
        "tie_on_baseline_fraction": rates[0] == rates[1] if None not in rates else None,
    }


def plot(data):
    # Units and visual frame are deliberately fixed for the published exercise.
    if tuple(data) != ("Oak", "Harbor") or max(max(pair) for pair in data.values()) > 100:
        raise ValueError("Published figure requires Oak, Harbor and a 0–100 range")
    add = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="700" height="425" viewBox="0 0 700 425" role="img" aria-labelledby="title desc">',
        '<title id="title">Reported library visits by window</title>',
        '<desc id="desc">Grouped bars for two reporting windows. Oak: 40 before, 50 after. Harbor: 80 before, 90 after. Values count visits, not people.</desc>',
        '<rect width="700" height="425" fill="#ffffff"/>',
        '<g font-family="system-ui, sans-serif" fill="#181e29">',
        '<text x="26" y="36" font-size="25" font-weight="700">Reported library visits by window</text>',
        '<text x="27" y="59" font-size="15">Two equally long reporting windows · Synthetic case</text>',
        '<rect x="28" y="76" width="22" height="14" fill="#ffffff" stroke="#24537c" stroke-width="2"/>',
        '<text x="56" y="89" font-size="15">Before</text>',
        '<rect x="127" y="76" width="22" height="14" fill="#24537c"/>',
        '<text x="155" y="89" font-size="15">After</text>',
        '<text x="30" y="116" font-size="14">Visits</text>',
    ]
    for count in (0, 20, 40, 60, 80, 100):
        y = 352 - 2 * count
        add.extend((
            f'<path d="M88 {y}H674" stroke="#a2aab5"/>',
            f'<text x="78" y="{y + 5}" text-anchor="end" font-size="14">{count}</text>',
        ))
    for (name, values), center in zip(data.items(), (239, 520)):
        for window, value, x, fill in zip(
            ("Before", "After"), values, (center - 79, center + 3), ("#ffffff", "#24537c")
        ):
            y = 352 - 2 * value
            add.extend((
                f'<rect id="{name}-{window}" x="{x}" y="{y}" width="76" height="{2 * value}" fill="{fill}" stroke="#24537c" stroke-width="2"/>',
                f'<text id="{name}-{window}-value" x="{x + 38}" y="{y - 9}" text-anchor="middle" font-size="17" font-weight="700">{value}</text>',
            ))
        add.append(f'<text x="{center}" y="385" text-anchor="middle" font-size="18" font-weight="700">{name}</text>')
    add.extend(("</g>", "</svg>"))
    # Keep accessible alternate text in sync with values if fixture changes.
    alt = " ".join(f"{name}: {b} before, {a} after." for name, (b, a) in data.items())
    add[2] = f'<desc id="desc">Grouped bars for two reporting windows. {alt} Values count visits, not people.</desc>'
    return "\n".join(add) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--svg", action="store_true", help="emit lesson figure to stdout instead of JSON")
    args = parser.parse_args(argv)
    try:
        data = read_visits(args.fixture)
        if args.svg:
            sys.stdout.write(plot(data))
        else:
            print(json.dumps(compare(data), indent=2))
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"Fixture rejected: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
