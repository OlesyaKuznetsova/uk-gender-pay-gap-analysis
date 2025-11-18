import pandas as pd

# Load processed dataset with sectors
df = pd.read_csv("data/processed/combined_with_sector.csv")

# Column name for gender pay gap (median hourly percent)
col = "GenderPayGap_HourlyPay_Median_Percent"

# Sort: worst companies first (largest gap where women earn less)
worst = df.sort_values(by=col, ascending=False).head(10)

# Sort: best companies (lowest gap, maybe negative)
best = df.sort_values(by=col, ascending=True).head(10)

print("\n=== WORST COMPANIES (largest pay gap against women) ===")
print(worst[["EmployerName", "Sector", "Year", col]])

print("\n=== BEST COMPANIES (smallest or negative pay gap) ===")
print(best[["EmployerName", "Sector", "Year", col]])

# Save results
worst.to_csv("data/processed/worst_companies.csv", index=False)
best.to_csv("data/processed/best_companies.csv", index=False)

print("\nFiles saved:")
print(" - data/processed/worst_companies.csv")
print(" - data/processed/best_companies.csv")
