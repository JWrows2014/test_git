#!/usr/bin/env python3
"""Generate a Tooth Growth boxplot from a CSV file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import seaborn as sns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a boxplot of tooth length by dosage with supplement type "
            "shown in the legend."
        )
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to a CSV file containing Tooth Growth data.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("tooth_growth_boxplot.png"),
        help="Output image path. Defaults to tooth_growth_boxplot.png.",
    )
    return parser.parse_args()


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_map = {
        "len": "ToothLength",
        "toothlength": "ToothLength",
        "tooth_length": "ToothLength",
        "dose": "Dose",
        "dosage": "Dose",
        "supp": "Supplement",
        "supplement": "Supplement",
        "supplementtype": "Supplement",
        "supplement_type": "Supplement",
    }

    renamed = {}
    for column in df.columns:
        key = column.strip().lower().replace(" ", "").replace("-", "").replace(".", "")
        if key in column_map:
            renamed[column] = column_map[key]

    df = df.rename(columns=renamed)

    required_columns = {"ToothLength", "Dose", "Supplement"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Missing required columns: {missing_list}. "
            "Expected columns representing tooth length, dose, and supplement type."
        )

    return df


def build_plot(df: pd.DataFrame, output_path: Path) -> None:
    dose_order = sorted(df["Dose"].astype(str).unique(), key=lambda value: float(value))
    plot_df = df.assign(Dose=df["Dose"].astype(str))

    sns.set_theme(style="whitegrid")
    ax = sns.boxplot(
        data=plot_df,
        x="Dose",
        y="ToothLength",
        hue="Supplement",
        order=dose_order,
    )

    ax.set_xlabel("Dosage")
    ax.set_ylabel("Tooth Length")
    ax.set_title("Tooth Length Distribution by Dosage and Supplement Type")
    ax.legend(title="Supplement Type")

    ax.figure.tight_layout()
    ax.figure.savefig(output_path, dpi=300)
    ax.figure.clf()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input_csv)
    df = normalize_columns(df)
    build_plot(df, args.output)
    print(f"Saved boxplot to {args.output}")


if __name__ == "__main__":
    main()
