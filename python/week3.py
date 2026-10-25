from pathlib import Path
import pandas as pd

# Project folders
project_folder = Path(__file__).resolve().parent.parent
output_folder = project_folder / "output"

# Week 1 files
sold_file = output_folder / "combined_residential_sold.csv"
listings_file = output_folder / "combined_residential_listings.csv"

# Read the Week 1 datasets
sold = pd.read_csv(sold_file, low_memory=False)
listings = pd.read_csv(listings_file, low_memory=False)

print("Week 1 datasets loaded.")

# Step 1: Download mortgage data from FRED
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(url)

# Rename the FRED columns
mortgage = mortgage.rename(columns={
    "observation_date": "date",
    "MORTGAGE30US": "rate_30yr_fixed"
})

# Convert the date column to a date
mortgage["date"] = pd.to_datetime(mortgage["date"])

# Step 2: Create monthly mortgage averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage
    .groupby("year_month", as_index=False)["rate_30yr_fixed"]
    .mean()
)

print("Monthly mortgage averages created.")

# Step 3: Create year_month for the sold dataset
sold["CloseDate"] = pd.to_datetime(
    sold["CloseDate"],
    errors="coerce"
)

sold["year_month"] = sold["CloseDate"].dt.to_period("M")

# Step 3: Create year_month for the listings dataset
listings["ListingContractDate"] = pd.to_datetime(
    listings["ListingContractDate"],
    errors="coerce"
)

listings["year_month"] = (
    listings["ListingContractDate"]
    .dt.to_period("M")
)

# Step 4: Merge mortgage rates onto both datasets
sold_with_rates = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

listings_with_rates = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

# Step 5: Check for missing mortgage rates
sold_missing_rates = (
    sold_with_rates["rate_30yr_fixed"]
    .isnull()
    .sum()
)

listings_missing_rates = (
    listings_with_rates["rate_30yr_fixed"]
    .isnull()
    .sum()
)

print("\nMissing mortgage rates:")
print("Sold:", sold_missing_rates)
print("Listings:", listings_missing_rates)

# Stop the program if the merge produced missing rates
if sold_missing_rates > 0 or listings_missing_rates > 0:
    print("\nSome rows did not receive a mortgage rate.")

    print("\nSold months without rates:")
    print(
        sold_with_rates[
            sold_with_rates["rate_30yr_fixed"].isnull()
        ]["year_month"].value_counts()
    )

    print("\nListing months without rates:")
    print(
        listings_with_rates[
            listings_with_rates["rate_30yr_fixed"].isnull()
        ]["year_month"].value_counts()
    )

    raise ValueError(
        "Mortgage-rate merge is incomplete."
    )

# Preview the merged sold dataset
print("\nSold dataset preview:")
print(
    sold_with_rates[
        [
            "CloseDate",
            "year_month",
            "ClosePrice",
            "rate_30yr_fixed"
        ]
    ].head()
)

# Save the enriched datasets
sold_output = output_folder / "enriched_residential_sold.csv"
listings_output = output_folder / "enriched_residential_listings.csv"

sold_with_rates.to_csv(sold_output, index=False)
listings_with_rates.to_csv(listings_output, index=False)

print("\nEnriched files saved:")
print(sold_output)
print(listings_output)

print("\nWeek 3 completed successfully.")