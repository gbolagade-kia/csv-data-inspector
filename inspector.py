import operator
from pathlib import Path

import pandas as pd

OPERATIONS = {
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
}


def inspect_column(df):
    if input("\nInspect a column? (y/n): ").strip().lower() != "y":
        return

    column = input("Enter the column name: ").strip()
    if column not in df.columns:
        print(f"Column not found: {column}")
        return

    print(df[column].to_string(index=False))


def filter_rows(df):
    if input("\nFilter the rows? (y/n): ").strip().lower() != "y":
        return df

    numeric_columns = df.select_dtypes(include="number").columns
    if numeric_columns.empty:
        print("This file has no numeric columns to filter.")
        return df

    print("Numeric columns:", ", ".join(numeric_columns))

    while True:
        column = input("Enter a numeric column, or press Enter to skip: ").strip()
        if not column:
            return df
        if column in numeric_columns:
            break
        print("Choose one of the numeric columns listed above.")

    while True:
        comparison = input("Choose an operator (>, <, ==, >=, <=): ").strip()
        if comparison in OPERATIONS:
            break
        print("Please choose an operator from the list.")

    while True:
        try:
            value = float(input("Enter a number to compare against: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    matches = OPERATIONS[comparison](df[column], value)
    filtered_df = df.loc[matches]

    print(f"\nMatching rows: {len(filtered_df)} of {len(df)}")
    if not filtered_df.empty:
        print(filtered_df.head(10).to_string(index=False))
        if len(filtered_df) > 10:
            print("Showing the first 10 matches. The export includes all matches.")

    return filtered_df


def main():
    entered_path = input("Enter the path to your CSV file: ").strip().strip('"')
    if not entered_path:
        print("Please enter a CSV file path.")
        return

    csv_path = Path(entered_path).expanduser()

    try:
        df = pd.read_csv(csv_path)
    except (OSError, UnicodeError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        print(f"Could not read the CSV: {error}")
        return

    # Treat cells containing only whitespace as missing.
    df = df.replace(r"^\s*$", float("nan"), regex=True)

    print(f"\nFile: {csv_path.name}")
    print(f"Rows: {len(df)}")
    print(f"Columns ({len(df.columns)}): {', '.join(df.columns)}")
    print("\nMissing values by column:")
    print(df.isna().sum().to_string())

    numeric_data = df.select_dtypes(include="number")
    if numeric_data.shape[1] > 0:
        print("\nNumeric summary:")
        print(numeric_data.describe().to_string())
    else:
        print("\nNo numeric columns to summarize.")

    inspect_column(df)
    result = filter_rows(df)

    output_path = csv_path.with_name(f"{csv_path.stem}_export.csv")
    try:
        result.to_csv(output_path, index=False, mode="x")
    except FileExistsError:
        print(f"\nExport already exists: {output_path}")
        print("Rename the existing export before running the script again.")
    except OSError as error:
        print(f"\nCould not save the export: {error}")
    else:
        print(f"\nSaved {len(result)} rows to {output_path}")


if __name__ == "__main__":
    main()