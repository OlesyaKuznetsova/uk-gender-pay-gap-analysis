import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset with sectors
df = pd.read_csv("data/processed/combined_with_sector.csv")

# Make sure Year is treated as a string for proper order
df["Year"] = df["Year"].astype(str)

# Group data: average Median Hourly Pay Gap by Sector and Year
grouped = (
    df.groupby(["Year", "Sector"])["GenderPayGap_HourlyPay_Median_Percent"]
    .mean()
    .reset_index()
)

# Pivot for easy plotting
pivot = grouped.pivot(index="Year", columns="Sector", values="GenderPayGap_HourlyPay_Median_Percent")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(pivot.index, pivot["Tech"], marker="o", color="#2D8EFF", linewidth=2, label="Tech Sector")
plt.plot(pivot.index, pivot["Healthcare"], marker="o", color="#FF5C8D", linewidth=2, label="Healthcare Sector")

# Styling
plt.title("Gender Pay Gap (Median %) Trends by Sector, 2018–2025", fontsize=14, weight="bold")
plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Median Hourly Pay Gap (%)", fontsize=12)
plt.grid(alpha=0.3)
plt.legend(title="Sector")
plt.tight_layout()

# Save chart
plt.savefig("data/processed/gender_pay_gap_trends.png", dpi=300)
plt.show()
