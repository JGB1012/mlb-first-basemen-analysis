import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "first_basemen_stats.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_FILE)

# -----------------------------
# Basic cleaning
# -----------------------------
numeric_cols = ["G", "PA", "AVG", "OBP", "SLG", "OPS", "HR", "RBI", "WAR"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# -----------------------------
# Create a simple composite score
# -----------------------------
# Normalize selected metrics so they are on similar scales
metrics = ["OPS", "HR", "RBI", "WAR", "OBP", "SLG"]

for metric in metrics:
    mean_val = df[metric].mean()
    std_val = df[metric].std()
    df[f"{metric}_z"] = (df[metric] - mean_val) / std_val

# Weighted score
df["Overall_Score"] = (
    0.30 * df["OPS_z"] +
    0.15 * df["HR_z"] +
    0.15 * df["RBI_z"] +
    0.25 * df["WAR_z"] +
    0.075 * df["OBP_z"] +
    0.075 * df["SLG_z"]
)

df = df.sort_values("Overall_Score", ascending=False)

# -----------------------------
# Save ranked table
# -----------------------------
ranked_file = OUTPUT_DIR / "ranked_first_basemen.csv"
df.to_csv(ranked_file, index=False)

print("Top First Basemen by Overall Score:")
print(df[["Player", "Team", "OPS", "HR", "RBI", "WAR", "Overall_Score"]].head(10))

# -----------------------------
# Plot 1: OPS by player
# -----------------------------
plt.figure(figsize=(10, 6))
plt.bar(df["Player"], df["OPS"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("OPS")
plt.title("OPS of MLB First Basemen")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "ops_bar_chart.png")
plt.close()

# -----------------------------
# Plot 2: HR vs WAR
# -----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df["HR"], df["WAR"])

for _, row in df.iterrows():
    plt.annotate(row["Player"], (row["HR"], row["WAR"]), fontsize=8)

plt.xlabel("Home Runs")
plt.ylabel("WAR")
plt.title("Home Runs vs WAR for MLB First Basemen")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "hr_vs_war_scatter.png")
plt.close()

# -----------------------------
# Plot 3: Overall score ranking
# -----------------------------
plt.figure(figsize=(10, 6))
plt.bar(df["Player"], df["Overall_Score"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Overall Score")
plt.title("Overall Ranking of MLB First Basemen")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "overall_score_ranking.png")
plt.close()

print(f"\nSaved outputs to: {OUTPUT_DIR}")