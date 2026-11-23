# CSV Data Inspector

A Python command-line tool for exploring CSV files before opening a notebook. It reports row counts, column names, missing values, and summary statistics for numeric columns.

## Getting started

Install Python 3, then open a terminal in the folder containing `inspector.py`:

```bash
python -m pip install pandas
python inspector.py
```

Enter a CSV file path when prompted. You can use a filename such as `sample.csv` if the file is in your current directory.

## Inspect and filter

- Inspect a column by entering its exact name when prompted.
- Optionally filter rows by comparing a numeric column to a number. Supported operators are `>`, `<`, `==`, `>=`, and `<=`.
- The tool previews up to 10 matching rows and exports every match. If you skip filtering, it exports all rows.
- Whitespace-only cells are treated as missing values. The export is saved beside the input as `<filename>_export.csv`. If that file already exists, rename it before running again.

## Example

Create a file named `sample.csv`:

```csv
name,score
Ada,85
Tomi,60
Zainab,92
```

Run the script and enter `sample.csv`. Skip the column inspection or choose `score`. When asked to filter, enter `y`, then enter `score`, `>`, and `70` at the prompts.

The resulting `sample_export.csv` contains:

```csv
name,score
Ada,85
Zainab,92
```
