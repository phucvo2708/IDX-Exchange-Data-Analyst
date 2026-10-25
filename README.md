# IDX-Exchange-Data-Analyst
This repository contains the code and documentation developed during my IDX Exchange Data Analyst Internship. The project focuses on cleaning, analyzing, and visualizing MLS real estate data using Python, Pandas, and Tableau.
MLS data is confidential, so raw data files and credentials are not included in this public repository

# Week 0:
*Week 0 focused on setting up the MLS data environment and verifying the monthly CRMLS datasets before analysis.

## Files

- `python/check_week0.py` checks whether monthly listing and sold files are present.
- `python/crmls_listed.py` extracts MLS listing data.
- `python/crmls_sold.py` extracts MLS sold data.
- Monthly CSV files are stored locally in the `csv` folder and are not included in this repository.

## Week 0 Tasks Completed

- Organized the project folders.
- Downloaded the available monthly listing and sold datasets.
- Checked the available months for both dataset types.
- Identified any missing monthly files.
- Reviewed the MLS data pipeline and property metadata.
- Prepared the project for Week 1 dataset aggregation.

# Week 1: 
Week 1 combined the monthly MLS listing and sold datasets into unified datasets for analysis.

## Tasks Completed

- Loaded monthly listing files from January 2024 through the latest available month.
- Loaded monthly sold files for the same period.
- Combined the monthly listing files into one dataset.
- Combined the monthly sold files into one dataset.
- Recorded row counts before and after concatenation.
- Filtered both datasets to include only records where:

# Week 2: 
Week 2 focused on inspecting the combined residential datasets before further cleaning and analysis.

## Tasks Completed

- Checked the number of rows and columns.
- Reviewed column names and data types.
- Reviewed the property types in the datasets.
- Flagged columns with more than 90% missing values.
- Created numeric summaries for important real estate fields.
- Generated histograms and boxplots to examine distributions and possible outliers.
- Saved validation reports and charts locally.

# Week 3:
Week 3 added monthly mortgage-rate information to the combined MLS datasets.

## Tasks Completed
- Fetched the weekly MORTGAGE30US series from the Federal Reserve Economic Data website.
- Converted the weekly mortgage rates into monthly averages.
- Created a year_month key for the mortgage data.
- Created a matching year_month key for the sold dataset using CloseDate.
- Created a matching year_month key for the listings dataset using ListingContractDate.
- Merged the monthly mortgage rates onto both MLS datasets.
- Checked for missing mortgage rates after the merge.
- Saved enriched sold and listing datasets locally.
