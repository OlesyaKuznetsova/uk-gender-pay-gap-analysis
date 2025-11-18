import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/processed/combined_with_sector.csv")

plt.figure(figsize=(9, 6))

# Create boxplot
df.boxplot(
    column=["GenderPayGap_HourlyPay_Median_Percent"],
    by="Sector"
)

plt.title("Median Hourly Pay Gap (%) by Sector (Tech vs Healthcare)")
plt.suptitle("")   # remove default ugly subtitle
plt.xlabel("Sector")
plt.ylabel("Median Hourly Pay Gap (%)")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

