from pathlib import Path
import re

DATA_FOLDER = Path(__file__).resolve().parent.parent / "csv"


def check_files(prefix):
    months = []

    for file in DATA_FOLDER.glob(f"{prefix}*.csv"):
        match = re.search(r"(\d{6})(?:_filled)?\.csv$", file.name)

        if match:
            months.append(match.group(1))

    months = sorted(set(months))

    print(f"\n{prefix}")
    print("Months found:")
    print(months)

    if not months:
        print("No files found.")
        return

    last_year = int(months[-1][:4])
    last_month = int(months[-1][4:])

    expected = []

    year = 2024
    month = 1

    while (year, month) <= (last_year, last_month):
        expected.append(f"{year}{month:02d}")

        month += 1

        if month == 13:
            month = 1
            year += 1

    missing = sorted(set(expected) - set(months))

    if missing:
        print("Missing months:")
        print(missing)
    else:
        print("No months are missing.")


check_files("CRMLSListing")
check_files("CRMLSSold")