import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/processed/combined_with_sector.csv")

# Column to use
gap_col = "GenderPayGap_HourlyPay_Median_Percent"

# Pivot table: rows = employers, columns = years
pivot_df = df.pivot_table(
    index="EmployerName_norm",
    columns="Year",
    values=gap_col
)

# Sort rows by average gap (optional but helps visually)
pivot_df = pivot_df.reindex(pivot_df.mean(axis=1).sort_values(ascending=False).index)

# Set up heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(
    pivot_df,
    cmap="coolwarm",      # blue = women earn more, red = men earn more
    center=0,             # 0 becomes white
    linewidths=0.3,
    linecolor='gray',
    cbar_kws={"label": "Median Hourly Pay Gap (%)"}
)

plt.title("Gender Pay Gap Heatmap (Median %), 2018–2025")
plt.xlabel("Financial Year")
plt.ylabel("Employer")

plt.tight_layout()
plt.show()

# Optionally save
plt.savefig("data/processed/heatmap_gender_gap.png")
