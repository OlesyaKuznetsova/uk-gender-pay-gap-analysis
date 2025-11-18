import pandas as pd

df = pd.read_csv("data/processed/combined_with_sector.csv")

print("Columns:")
print(df.columns.tolist())

print("\nCount by Sector:")
print(df["Sector"].value_counts())

print("\nMissing values in Median column:")
print(df["GenderPayGap_HourlyPay_Median_Percent"].isna().sum())

print("\nUnique Years:")
print(df["Year"].unique())

print("\nPreview:")
print(df[["EmployerName", "Sector", "Year", "GenderPayGap_HourlyPay_Median_Percent"]].head(20))
