from pathlib import Path
import pandas as pd
import re

# Project folders
BASE_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_FOLDER / "csv"
OUTPUT_FOLDER = BASE_FOLDER / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)


def find_monthly_files(prefix):
    """
    Finds monthly files and handles names such as:

    CRMLSSold202401.csv
    CRMLSSold202401_filled.csv
    """

    files_by_month = {}

    for file in DATA_FOLDER.glob(f"{prefix}*.csv"):
        match = re.search(r"(\d{6})(?:_filled)?\.csv$", file.name)

        if match:
            month = match.group(1)

            # Prefer the _filled file if both versions exist
            if month not in files_by_month:
                files_by_month[month] = file
            elif "_filled" in file.name:
                files_by_month[month] = file

    return [
        files_by_month[month]
        for month in sorted(files_by_month)
    ]


def combine_and_filter(prefix, output_filename):
    files = find_monthly_files(prefix)

    if not files:
        raise FileNotFoundError(
            f"No files found for prefix: {prefix}"
        )

    print(f"\nProcessing {prefix} files")
    print("-" * 40)

    dataframes = []
    rows_before_concat = 0

    for file in files:
        print(f"Reading: {file.name}")

        df = pd.read_csv(file)

        print(f"Rows in file: {len(df):,}")

        rows_before_concat += len(df)
        dataframes.append(df)

    # Combine all monthly files
    combined = pd.concat(dataframes, ignore_index=True)

    print(f"\nNumber of files: {len(files)}")
    print(f"Rows before concatenation: {rows_before_concat:,}")
    print(f"Rows after concatenation: {len(combined):,}")

    # Confirm that PropertyType exists
    if "PropertyType" not in combined.columns:
        raise KeyError(
            "The PropertyType column was not found."
        )

    print("\nProperty types found:")
    print(combined["PropertyType"].value_counts(dropna=False))

    # Filter to Residential properties
    rows_before_filter = len(combined)

    residential = combined[
        combined["PropertyType"]
        .astype("string")
        .str.strip()
        .eq("Residential")
    ].copy()

    rows_after_filter = len(residential)

    print(f"\nRows before Residential filter: {rows_before_filter:,}")
    print(f"Rows after Residential filter: {rows_after_filter:,}")

    # Save the final dataset
    output_path = OUTPUT_FOLDER / output_filename
    residential.to_csv(output_path, index=False)

    print(f"Saved to: {output_path}")
    print(f"Final rows saved: {len(residential):,}")

    return residential


# Combine sold datasets
sold = combine_and_filter(
    prefix="CRMLSSold",
    output_filename="combined_residential_sold.csv"
)

# Combine listing datasets
listings = combine_and_filter(
    prefix="CRMLSListing",
    output_filename="combined_residential_listings.csv"
)

print("\nWeek 1 completed successfully.")