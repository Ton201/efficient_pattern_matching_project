#!/usr/bin/env python3

import csv
import time
import argparse
from pathlib import Path
from tqdm import tqdm

from SAM import SuffixAutomaton


DATASET_DIRNAMES = ["dna", "english", "mono", "random"]


def dataset_paths(root: Path, name: str):
    """
    Given dataset root and dataset name (e.g. 'dna'),
    return paths to:
        - text file:      <name>1MB.txt
        - patterns file:  <name>1MB_patterns.txt
        - C++ baseline:      naive.csv
        - output csv:     sam_python.csv
    """
    ddir = root / name
    if not ddir.is_dir():
        raise FileNotFoundError(f"Dataset directory {ddir} not found")

    text_path = ddir / f"{name}1MB.txt"
    patterns_path = ddir / f"{name}1MB_patterns.txt"
    naive_csv = ddir / "naive.csv"
    out_csv = ddir / "sam_python.csv"

    # Safety fallbacks if filenames differ slightly
    if not text_path.exists():
        candidates = list(ddir.glob("*1MB.txt"))
        if not candidates:
            raise FileNotFoundError(f"No *1MB.txt in {ddir}")
        text_path = candidates[0]

    if not patterns_path.exists():
        candidates = list(ddir.glob("*1MB_patterns.txt"))
        if not candidates:
            raise FileNotFoundError(f"No *1MB_patterns.txt in {ddir}")
        patterns_path = candidates[0]

    if not naive_csv.exists():
        raise FileNotFoundError(f"naive.csv not found in {ddir}")

    return text_path, patterns_path, naive_csv, out_csv


def load_patterns(patterns_path: Path):
    """
    One pattern per line, ignore empty lines and lines starting with '#'.
    """
    patterns = []
    with patterns_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def count_rows_in_naive(naive_path: Path) -> int:
    """
    Count data rows in naive.csv, skipping a header row if present.
    We don't depend on the exact column layout, just the number of rows.
    """
    with naive_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return 0

    # Try to detect a header: if first cell is not an int, assume header
    def is_int(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    start_idx = 1 if rows and rows[0] and not is_int(rows[0][0]) else 0
    return max(0, len(rows) - start_idx)


def measure(fn, *args, **kwargs):
    """
    Measure wall-clock time of fn(*args, **kwargs).
    Returns (elapsed_seconds, result).
    """
    t0 = time.perf_counter()
    res = fn(*args, **kwargs)
    t1 = time.perf_counter()
    return t1 - t0, res


def run_for_dataset(root: Path, name: str, max_patterns: int | None = None):
    print(f"\n=== Dataset: {name} ===")

    text_path, patterns_path, naive_csv, out_csv = dataset_paths(root, name)

    print(f"  text:     {text_path}")
    print(f"  patterns: {patterns_path}")
    print(f"  naive:    {naive_csv}")

    # 1) Build SAM over the text
    text = text_path.read_text(encoding="utf-8", errors="ignore")

    sa = SuffixAutomaton()
    build_time, _ = measure(sa.build, text)
    n_states = sa.n_states()
    n_trans = sa.n_transitions()

    print(f"  build time: {build_time:.4f}s, states={n_states}, transitions={n_trans}")

    # 2) Load patterns
    patterns = load_patterns(patterns_path)
    if max_patterns is not None:
        patterns = patterns[:max_patterns]

    n_patterns = len(patterns)
    print(f"  #patterns from *_patterns.txt: {n_patterns}")

    # 3) Sanity check vs naive.csv
    n_naive_rows = count_rows_in_naive(naive_csv)
    print(f"  #rows in naive.csv: {n_naive_rows}")

    if n_patterns != n_naive_rows:
        print(
            f"  WARNING: pattern count ({n_patterns}) != naive rows ({n_naive_rows})"
        )

    # 4) Run queries and write CSV with SAM timings
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "dataset",
            "pattern_index",
            "pattern",
            "pattern_length",
            "occurrences",
            "time_count_s",
            "time_match_first_s",
            "time_match_last_s",
            "time_match_all_s",
            "time_per_occurrence_match_all_s",  # match_all time / max(occ, 1)
            "build_time_s",
            "n_states",
            "n_transitions",
        ])

        # for i, pat in enumerate(patterns):
        #     if i % 10 == 0:
        #         print(f"    pattern {i}/{n_patterns}", end="\r")
        for i, pat in enumerate(tqdm(patterns, desc=f"{name}: patterns", unit="pat")):

            plen = len(pat)

            t_count, occ = measure(sa.count, pat)
            t_first, first_pos = measure(sa.match_first, pat)
            t_last, last_pos = measure(sa.match_last, pat)
            t_all, all_pos = measure(sa.match_all, pat)

            # Normalized match_all time per reported occurrence
            norm = t_all / occ if occ > 0 else t_all

            writer.writerow([
                name,
                i,
                pat,
                plen,
                occ,
                t_count,
                t_first,
                t_last,
                t_all,
                norm,
                build_time,
                n_states,
                n_trans,
            ])

    print(f"  -> wrote {out_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Run Python SuffixAutomaton experiments on selected datasets."
    )
    parser.add_argument(
        "datasets",
        nargs="*",
        help=(
            "Datasets to run: any subset of "
            + ", ".join(DATASET_DIRNAMES)
            + ". If omitted, runs all."
        ),
    )
    parser.add_argument(
        "--max-patterns",
        type=int,
        default=None,
        help="If set, only use the first N patterns per dataset.",
    )

    args = parser.parse_args()

    # Determine which datasets to run
    if not args.datasets:
        selected = DATASET_DIRNAMES
    else:
        # Validate manually so we can give a nicer error message
        invalid = [d for d in args.datasets if d not in DATASET_DIRNAMES]
        if invalid:
            raise SystemExit(
                f"Unknown dataset(s): {', '.join(invalid)}. "
                f"Allowed: {', '.join(DATASET_DIRNAMES)}"
            )
        selected = args.datasets

    repo_root = Path(__file__).resolve().parent.parent.parent  # repo/
    datasets_root = repo_root / "datasets"

    print(f"Datasets root: {datasets_root}")
    print(f"Selected datasets: {', '.join(selected)}")
    if args.max_patterns is not None:
        print(f"Max patterns per dataset: {args.max_patterns}")

    for name in selected:
        run_for_dataset(datasets_root, name, max_patterns=args.max_patterns)


if __name__ == "__main__":
    main()
