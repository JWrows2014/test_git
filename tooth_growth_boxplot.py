#!/usr/bin/env python3
"""Generate a Tooth Growth boxplot from the local CSV file."""

import pandas as pd
import seaborn as sns


df = pd.read_csv("toothgrowth.csv").rename(
    columns={
        "len": "ToothLength",
        "dose": "Dose",
        "supp": "Supplement",
    }
)

dose_order = sorted(df["Dose"].astype(str).unique(), key=float)
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
ax.figure.savefig("tooth_growth_boxplot.png", dpi=300)
ax.figure.clf()

print("Saved boxplot to tooth_growth_boxplot.png")
