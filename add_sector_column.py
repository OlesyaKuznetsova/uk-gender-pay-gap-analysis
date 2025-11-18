import pandas as pd

# Load the combined dataset
df = pd.read_csv("data/processed/combined_2018_2024.csv")

# Define tech and healthcare companies
tech = [
    "ARM LIMITED",
    "BRITISH BROADCASTING CORPORATION",
    "BRITISH TELECOMMUNICATIONS PUBLIC LIMITED COMPANY",
    "GOOGLE UK LIMITED",
    "IBM UNITED KINGDOM LIMITED",
    "MICROSOFT LIMITED",
    "MONZO BANK LIMITED",
]

health = [
    "ASTRAZENECA UK LIMITED",
    "BARTS HEALTH NHS TRUST",
    "BUPA INSURANCE SERVICES LIMITED",
    "GLAXOSMITHKLINE SERVICES UNLIMITED",
    "GUY'S & ST THOMAS' NHS FOUNDATION TRUST",  
    "MANCHESTER UNIVERSITY NHS FOUNDATION TRUST",
    "SPIRE HEALTHCARE LIMITED",
]


# Normalize names (remove extra spaces, make uppercase)
df["EmployerName_norm"] = df["EmployerName"].str.strip().str.upper()

tech_norm = [x.upper() for x in tech]
health_norm = [x.upper() for x in health]

def classify_sector(name):
    if name in tech_norm:
        return "Tech"
    elif name in health_norm:
        return "Healthcare"
    else:
        return "Unknown"

df["Sector"] = df["EmployerName_norm"].apply(classify_sector)

# Save updated dataset
output_path = "data/processed/combined_with_sector.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(" Sector column added and file saved as:", output_path)
print(df[["EmployerName", "Sector", "Year"]].head(10))
