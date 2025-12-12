#!/usr/bin/env python3
"""
Plot experimental results comparing SAM vs naive algorithm.

Assumes naive.csv contains ONLY:
    length, occurences, time[ns]

and sam_python.csv contains the columns from run_experiments.py.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ================================================================
#  Helper functions
# ================================================================

def load_sam(dataset_dir: Path) -> pd.DataFrame:
    sam_csv = dataset_dir / "sam_python.csv"
    if not sam_csv.exists():
        raise FileNotFoundError(f"{sam_csv} not found.")
    return pd.read_csv(sam_csv)


def load_naive(dataset_dir: Path) -> pd.DataFrame:
    naive_csv = dataset_dir / "naive.csv"
    if not naive_csv.exists():
        raise FileNotFoundError(f"{naive_csv} not found.")

    df = pd.read_csv(naive_csv)

    expected_cols = {"length", "occurences", "time[ns]"}
    if not expected_cols.issubset(df.columns):
        raise ValueError(
            f"{naive_csv} must contain columns {expected_cols}, "
            f"but contains: {set(df.columns)}"
        )

    return df


def ensure_dir(d: Path):
    d.mkdir(parents=True, exist_ok=True)


# ================================================================
#  Plotting
# ================================================================

def plot_length_vs_time(df, dataset, outpath):
    plt.figure(figsize=(8, 5))

    plt.scatter(df["length"], df["time_per_occ_naive"], label="Naive", alpha=0.7)
    plt.scatter(df["length"], df["time_per_occ_sam"], label="SAM", alpha=0.7)

    plt.xlabel("Pattern length")
    plt.ylabel("Time per occurrence [s]")
    plt.title(f"{dataset}: Pattern length vs time per occurrence")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_occ_vs_time(df, dataset, outpath):
    plt.figure(figsize=(8, 5))

    plt.scatter(df["occurences"], df["time_per_occ_naive"], label="Naive", alpha=0.7)
    plt.scatter(df["occurences"], df["time_per_occ_sam"], label="SAM", alpha=0.7)

    plt.xlabel("Number of occurrences")
    plt.ylabel("Time per occurrence [s]")
    plt.title(f"{dataset}: Occurrences vs time per occurrence")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_global_metrics(summary_df, outroot):
    # Build time per dataset
    plt.figure(figsize=(8, 5))
    plt.bar(summary_df["dataset"], summary_df["build_time_s"])
    plt.xlabel("Dataset")
    plt.ylabel("Build time [s]")
    plt.title("SAM build time per dataset")
    plt.tight_layout()
    plt.savefig(outroot / "sam_build_time.png")
    plt.close()

    # Automaton size
    plt.figure(figsize=(8, 5))
    x = range(len(summary_df))
    width = 0.4

    plt.bar([i - width/2 for i in x], summary_df["n_states"], 
            label="states", width=width)
    plt.bar([i + width/2 for i in x], summary_df["n_transitions"],
            label="transitions", width=width)

    plt.xticks(list(x), summary_df["dataset"])
    plt.xlabel("Dataset")
    plt.ylabel("Count")
    plt.title("SAM size per dataset")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outroot / "sam_size.png")
    plt.close()


# ================================================================
#  Main
# ================================================================

def process_dataset(root: Path, dataset: str, outroot: Path):
    print(f"\n=== {dataset} ===")
    ddir = root / dataset

    sam = load_sam(ddir)
    naive = load_naive(ddir)

    # Merge: naive rows are in the same order as patterns
    # so we just attach them by index (pattern strings not present)
    merged = pd.concat([naive.reset_index(drop=True),
                        sam.reset_index(drop=True)], axis=1)

    # Convert time[ns] → seconds
    merged["time_naive_s"] = merged["time[ns]"] / 1e9

    # Compute per-occ times
    merged["time_per_occ_naive"] = merged["time_naive_s"] / merged["occurences"].clip(lower=1)
    merged["time_per_occ_sam"] = merged["time_per_occurrence_match_all_s"]

    # Output directory
    outdir = outroot / dataset
    ensure_dir(outdir)

    # Plots
    plot_length_vs_time(merged, dataset, outdir / f"{dataset}_len_vs_time.png")
    plot_occ_vs_time(merged, dataset, outdir / f"{dataset}_occ_vs_time.png")

    # Summary row for global metrics
    s0 = sam.iloc[0]
    return {
        "dataset": dataset,
        "build_time_s": float(s0["build_time_s"]),
        "n_states": int(s0["n_states"]),
        "n_transitions": int(s0["n_transitions"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Visualize SAM vs naive results")
    parser.add_argument(
        "datasets",
        nargs="*",
        help="Datasets to plot (dna english moni random). If omitted, auto-detect."
    )
    parser.add_argument(
        "--datasets-root",
        type=str,
        default="./datasets",
        help="Root directory of datasets (default: ./datasets)."
    )
    parser.add_argument(
        "--output-root",
        type=str,
        default="./datasets",
        help="Where to store plot images (default: inside each dataset dir)."
    )
    args = parser.parse_args()

    datasets_root = Path(args.datasets_root).resolve()
    outroot = Path(args.output_root).resolve()

    # Auto-detect datasets if none given
    if args.datasets:
        datasets = args.datasets
    else:
        datasets = [
            d.name for d in datasets_root.iterdir()
            if (datasets_root / d / "sam_python.csv").exists()
            and (datasets_root / d / "naive.csv").exists()
        ]

    summaries = []
    for ds in datasets:
        summaries.append(process_dataset(datasets_root, ds, outroot))

    # Global summary plots
    plot_global_metrics(pd.DataFrame(summaries), outroot)


if __name__ == "__main__":
    main()
