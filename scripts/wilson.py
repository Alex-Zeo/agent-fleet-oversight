#!/usr/bin/env python3
import argparse
import csv
import math
import sys

Z95 = 1.959963984540054
AGREEMENT_BAR = 0.85
LOWER_BOUND_BAR = 0.75

PUBLISHED_ROWS = [
    ("Single picks, blinded options: judge", 8, 24),
    ("Single picks: chance (1 of 4)", 6, 24),
    ("Single picks: always option 1", 7, 24),
    ("Single picks: fewest hits that clear the rule", 23, 24),
    ("Single picks: one hit fewer", 22, 24),
    ("Accept or send back: judge", 28, 56),
    ("Accept or send back: always send back", 37, 56),
]


def wilson(hits, n, z=Z95):
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= hits <= n:
        raise ValueError("hits must be between 0 and n")
    p = hits / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def clears_rule(hits, n):
    low, _ = wilson(hits, n)
    return hits / n >= AGREEMENT_BAR and low >= LOWER_BOUND_BAR


def fewest_hits_to_clear(n):
    for hits in range(n + 1):
        if clears_rule(hits, n):
            return hits
    return None


def row(label, hits, n):
    low, high = wilson(hits, n)
    verdict = "clears" if clears_rule(hits, n) else "does not clear"
    return f"{label:<48} {hits:>3}/{n:<3} {100 * hits / n:5.1f}%  {100 * low:5.1f}% to {100 * high:5.1f}%  {verdict}"


def score_csv(path):
    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        missing = {"prediction", "truth"} - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path}: missing columns {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise SystemExit(f"{path}: no rows")
    hits = sum(1 for r in rows if r["prediction"].strip() == r["truth"].strip())
    truths = [r["truth"].strip() for r in rows]
    majority = max(set(truths), key=truths.count)
    baseline = truths.count(majority)
    print(row("Judge", hits, len(rows)))
    print(row(f"Always '{majority}'", baseline, len(rows)))


def main(argv):
    parser = argparse.ArgumentParser(
        description="Wilson 95% intervals and the judge-check decision rule (85% agreement, lower bound 75%)."
    )
    parser.add_argument("--hits", type=int)
    parser.add_argument("--n", type=int)
    parser.add_argument("--csv", help="CSV with columns prediction,truth; scores hits against the majority-answer baseline")
    args = parser.parse_args(argv)
    if args.csv:
        score_csv(args.csv)
        return 0
    if args.hits is not None or args.n is not None:
        if args.hits is None or args.n is None:
            parser.error("--hits and --n go together")
        print(row("Given", args.hits, args.n))
        return 0
    for label, hits, n in PUBLISHED_ROWS:
        print(row(label, hits, n))
    for n in (24, 40, 56, 150):
        print(f"Fewest agreements that clear the rule at n={n}: {fewest_hits_to_clear(n)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
