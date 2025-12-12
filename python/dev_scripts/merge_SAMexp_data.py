#!/usr/bin/env python3
"""
Print a summary table of SAM metrics for each dataset:
dataset | construction_time | n_states | n_transitions
"""

import pandas as pd
from pathlib import Path

def main():
    datasets_root = Path("./datasets").resolve()

    rows = []
    for dataset_dir in sorted(datasets_root.iterdir()):
        if not dataset_dir.is_dir():
            continue

        csv_path = dataset_dir / "sam_python.csv"
        if not csv_path.exists():
            continue  # skip datasets without results

        df = pd.read_csv(csv_path)

        # All rows contain the same build_time/n_states/n_transitions, take row 0
        build_time = df.loc[0, "build_time_s"]
        n_states = df.loc[0, "n_states"]
        n_trans = df.loc[0, "n_transitions"]

        rows.append({
            "dataset": dataset_dir.name,
            "construction_time_s": round(build_time, 2),
            "n_states": int(n_states),
            "n_transitions": int(n_trans),
        })

    summary_df = pd.DataFrame(rows).set_index("dataset")

    print("\n=== Suffix Automaton Summary ===\n")
    print(summary_df.to_string())
    print()

if __name__ == "__main__":
    main()