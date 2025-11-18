import pandas as pd
from scipy.stats import ttest_ind

# Load dataset
df = pd.read_csv("data/processed/combined_with_sector.csv")

# Column to test
col = "GenderPayGap_HourlyPay_Median_Percent"

# Split by sector
tech = df[df["Sector"] == "Tech"][col]
health = df[df["Sector"] == "Healthcare"][col]

# Run t-test (independent samples)
t_stat, p_val = ttest_ind(tech, health, equal_var=False)

print("T-statistic:", t_stat)
print("P-value:", p_val)
