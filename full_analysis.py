import pandas as pd
import numpy as np
import glob
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind


#User confirmation function
def confirm_run():
    print("You are about to run the full analysis using CSV files in data/raw.")
    print("Make sure your files are correct before continuing.")
    answer = input("Do you want to continue? (y/n): ").strip().lower()

    if answer not in ["y", "yes"]:
        print("Analysis cancelled.")
        exit()
confirm_run()

#Configuration     

RAW_DATA_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

#Company lists for assigning sectors
#If you use your own datasets UPDATE THESE LISTS

TECH_COMPANIES = [
    "ARM LIMITED",
    "BRITISH BROADCASTING CORPORATION",
    "BRITISH TELECOMMUNICATIONS PUBLIC LIMITED COMPANY",
    "GOOGLE UK LIMITED",
    "IBM UNITED KINGDOM LIMITED",
    "MICROSOFT LIMITED",
    "MONZO BANK LIMITED",
]

HEALTHCARE_COMPANIES = [
    "ASTRAZENECA UK LIMITED",
    "BARTS HEALTH NHS TRUST",
    "BUPA INSURANCE SERVICES LIMITED",
    "GLAXOSMITHKLINE SERVICES UNLIMITED",
    "GUY'S & ST THOMAS' NHS FOUNDATION TRUST",
    "MANCHESTER UNIVERSITY NHS FOUNDATION TRUST",
    "SPIRE HEALTHCARE LIMITED",
]


#Load & combine CSV files       

def load_and_combine():
    files = sorted(glob.glob(f"{RAW_DATA_DIR}/*.csv"))
    all_data = []

    for file in files:
        try:
            df = pd.read_csv(file, encoding="utf-8-sig")
        except:
            df = pd.read_csv(file, encoding="utf-16", errors="ignore")

        df = df.dropna(how="all")

        year = Path(file).stem.split()[-1].replace(".csv", "")
        df["Year"] = year

        all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)
    output_path = f"{PROCESSED_DIR}/combined_2018_2024.csv"
    combined.to_csv(output_path, index=False, encoding="utf-8")

    print("Combined CSV saved:", output_path)
    return combined


#Add sector column 
#Adds a new column "Sector" based on employer name
#User can modify lists TECH_COMPANIES and HEALTHCARE_COMPANIES above     

def add_sector(df):
    df["EmployerName_norm"] = df["EmployerName"].str.strip().str.upper()

    tech_norm = [x.upper() for x in TECH_COMPANIES]
    health_norm = [x.upper() for x in HEALTHCARE_COMPANIES]

    def classify(name):
        if name in tech_norm:
            return "Tech"
        elif name in health_norm:
            return "Healthcare"
        else:
            return "Unknown"

    df["Sector"] = df["EmployerName_norm"].apply(classify)

    output = f"{PROCESSED_DIR}/combined_with_sector.csv"
    df.to_csv(output, index=False, encoding="utf-8")
    print("Added sector column:", output)

    return df


#Find best & worst companies    
#Top 10 worst companies (biggest pay gap against women)
#Top 10 best companies (smallest or negative gap)   

def find_best_worst(df):
    col = "GenderPayGap_HourlyPay_Median_Percent"

    worst = df.sort_values(by=col, ascending=False).head(10)
    best = df.sort_values(by=col, ascending=True).head(10)

    worst.to_csv(f"{PROCESSED_DIR}/worst_companies.csv", index=False)
    best.to_csv(f"{PROCESSED_DIR}/best_companies.csv", index=False)

    print("Saved best/worst companies tables.")

    return best, worst


#Built plots     
#Plot  1 - Line chart of median pay gap trends over time for Tech and Healthcare
#Shows the change across years

def plot_trends(df):
    df["Year"] = df["Year"].astype(str)
    grouped = df.groupby(["Year", "Sector"])["GenderPayGap_HourlyPay_Median_Percent"].mean().reset_index()

    pivot = grouped.pivot(index="Year", columns="Sector", values="GenderPayGap_HourlyPay_Median_Percent")

    plt.figure(figsize=(10, 6))
    plt.plot(pivot.index, pivot["Tech"], marker="o", label="Tech")
    plt.plot(pivot.index, pivot["Healthcare"], marker="o", label="Healthcare")

    plt.title("Gender Pay Gap Trends by Sector ")
    plt.xlabel("Year")
    plt.ylabel("Median Hourly Pay Gap (%)")
    plt.grid(alpha=0.3)
    plt.legend()

    out = f"{PROCESSED_DIR}/plot_trends_v2.png"
    plt.savefig(out, dpi=300)
    plt.close()

    print("Saved:", out)

#Plot  2 -  Heatmap of gender pay gap for each employer across years
#Useful to see companies with consistently high/low gaps

def plot_heatmap(df):
    gap_col = "GenderPayGap_HourlyPay_Median_Percent"

    pivot_df = df.pivot_table(index="EmployerName_norm", columns="Year", values=gap_col)
    pivot_df = pivot_df.reindex(pivot_df.mean(axis=1).sort_values(ascending=False).index)

    plt.figure(figsize=(18, 12))
    sns.heatmap(
        pivot_df,
        cmap="coolwarm",
        center=0,
        linewidths=0.3,
        cbar_kws={"label": "Median Hourly Pay Gap (%)"}
    )

    plt.title("Gender Pay Gap Heatmap")
    plt.xlabel("Year")
    plt.ylabel("Employer")

    out = f"{PROCESSED_DIR}/plot_heatmap_v2.png"

    plt.tight_layout()             
    plt.subplots_adjust(left=0.28) 
    plt.savefig(out, dpi=300)
    plt.close()

    print("Saved:", out)

#Plot 3 - Boxplot comparing distribution of pay gaps for Tech vs Healthcare
#Visualises difference in spread and medians

def plot_box(df):
    plt.figure(figsize=(9, 6))
    df.boxplot(
        column="GenderPayGap_HourlyPay_Median_Percent",
        by="Sector",
    )

    plt.title("Median Hourly Pay Gap by Sector ")
    plt.suptitle("")
    plt.ylabel("Median Pay Gap (%)")
    plt.grid(alpha=0.3)

    out = f"{PROCESSED_DIR}/plot_boxplot_v2.png"
    plt.savefig(out, dpi=300)
    plt.close()

    print("Saved:", out)


#Run Welch t-test
#Runs Welch's t-test to compare average pay gap between
#Tech and Healthcare sectors

def run_ttest(df):
    col = "GenderPayGap_HourlyPay_Median_Percent"

    tech = df[df["Sector"] == "Tech"][col]
    health = df[df["Sector"] == "Healthcare"][col]

    t_stat, p_val = ttest_ind(tech, health, equal_var=False)

    print("\n=== T-TEST RESULT ===")
    print("T-statistic:", t_stat)
    print("P-value:", p_val)

    return t_stat, p_val


#Main
#Full analysis pipeline

def main():
    df = load_and_combine()
    df = add_sector(df)

    find_best_worst(df)
    plot_trends(df)
    plot_heatmap(df)
    plot_box(df)
    run_ttest(df)

    print("\nAll analysis completed successfully.")


if __name__ == "__main__":
    main()

