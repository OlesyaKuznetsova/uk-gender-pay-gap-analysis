import pandas as pd
from pathlib import Path
import glob

# Folder where all yearly CSV files are stored
raw_path = Path("data/raw")

# Get all CSV files from the folder
files = sorted(glob.glob(str(raw_path / "*.csv")))

all_data = []

for file in files:
    print(f"🔹 Processing: {file}")
    try:
        df = pd.read_csv(file, encoding="utf-8-sig")
    except:
        df = pd.read_csv(file, encoding="utf-16", errors="ignore")

    # Remove completely empty rows (including NULL tails)
    df = df.dropna(how="all")

    # Extract year from the filename (e.g. ...2021-22.csv → 2021-22)
    year = file.split()[-1].replace(".csv", "")
    df["Year"] = year

    all_data.append(df)

# Combine all dataframes into one
combined = pd.concat(all_data, ignore_index=True)

# Save the final combined file
output_path = Path("data/processed/combined_2018_2024.csv")
combined.to_csv(output_path, index=False, encoding="utf-8")

print("Combined files:", len(files))
print("Saved as:", output_path)
print("Total rows:", len(combined))
print(combined.head(5))
