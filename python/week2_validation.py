from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project folders
BASE_FOLDER = Path(__file__).resolve().parent.parent
INPUT_FOLDER = BASE_FOLDER / "output"
REPORT_FOLDER = BASE_FOLDER / "week2_output"

REPORT_FOLDER.mkdir(exist_ok=True)


def validate_dataset(filename, dataset_name):
    input_path = INPUT_FOLDER / filename
    df = pd.read_csv(input_path, low_memory=False)

    print(f"\n===== {dataset_name} =====")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    # Display column names
    print("\nColumn names:")
    print(df.columns.tolist())

    # Display data types
    print("\nColumn data types:")
    print(df.dtypes)

    # Display property types
    if "PropertyType" in df.columns:
        print("\nProperty types:")
        print(df["PropertyType"].value_counts(dropna=False))

    # Missing-value report
    null_report = pd.DataFrame({
        "null_count": df.isnull().sum(),
        "null_percent": df.isnull().mean() * 100
    })

    null_report = null_report.sort_values(
        by="null_percent",
        ascending=False
    )

    null_report["over_90_percent_missing"] = (
        null_report["null_percent"] > 90
    )

    null_report.to_csv(
        REPORT_FOLDER / f"{dataset_name}_null_report.csv"
    )

    print("\nColumns with more than 90% missing values:")
    print(
        null_report[
            null_report["over_90_percent_missing"]
        ]
    )

    # Numeric fields required by the handbook
    numeric_columns = [
        "ClosePrice",
        "ListPrice",
        "OriginalListPrice",
        "LivingArea",
        "LotSizeAcres",
        "BedroomsTotal",
        "BathroomsTotalInteger",
        "DaysOnMarket",
        "YearBuilt"
    ]

    available_columns = [
        column for column in numeric_columns
        if column in df.columns
    ]

    numeric_data = df[available_columns].copy()

    for column in available_columns:
        numeric_data[column] = pd.to_numeric(
            numeric_data[column],
            errors="coerce"
        )

    # Numeric summary
    numeric_summary = numeric_data.describe(
        percentiles=[0.25, 0.50, 0.75]
    ).T

    numeric_summary.to_csv(
        REPORT_FOLDER / f"{dataset_name}_numeric_summary.csv"
    )

    print("\nNumeric summary:")
    print(numeric_summary)

    # Histograms and boxplots
    for column in available_columns:
        values = numeric_data[column].dropna()

        if values.empty:
            continue

        plt.figure(figsize=(8, 5))
        plt.hist(values, bins=40)
        plt.title(f"{dataset_name}: {column} Histogram")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(
            REPORT_FOLDER / f"{dataset_name}_{column}_histogram.png"
        )
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.boxplot(values, vert=False)
        plt.title(f"{dataset_name}: {column} Boxplot")
        plt.xlabel(column)
        plt.tight_layout()
        plt.savefig(
            REPORT_FOLDER / f"{dataset_name}_{column}_boxplot.png"
        )
        plt.close()

    # Save another copy of the validated dataset
    df.to_csv(
        REPORT_FOLDER / f"validated_{dataset_name}.csv",
        index=False
    )

    print(f"\nReports saved in: {REPORT_FOLDER}")


validate_dataset(
    "combined_residential_sold.csv",
    "sold"
)

validate_dataset(
    "combined_residential_listings.csv",
    "listings"
)

print("\nWeek 2 validation completed successfully.")