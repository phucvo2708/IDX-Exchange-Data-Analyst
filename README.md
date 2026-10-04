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

### Tasks Completed

- Loaded monthly listing files from January 2024 through the latest available month.
- Loaded monthly sold files for the same period.
- Combined the monthly listing files into one dataset.
- Combined the monthly sold files into one dataset.
- Recorded row counts before and after concatenation.
- Filtered both datasets to include only records where:
