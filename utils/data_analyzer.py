import pandas as pd


def analyze_csv(file_path):

    df = pd.read_csv(file_path)

    rows = df.shape[0]
    cols = df.shape[1]

    column_names = list(df.columns)

    missing_values = int(df.isnull().sum().sum())

    numeric_cols = df.select_dtypes(include=["number"])

    stats = ""

    if not numeric_cols.empty:
        stats = numeric_cols.describe().to_string()

    summary = f"""
📊 DATASET OVERVIEW

Rows: {rows}
Columns: {cols}

Column Names:
{', '.join(column_names)}

Missing Values:
{missing_values}

Description:
This dataset contains {rows} records and {cols} features.
The data includes information about:
{', '.join(column_names[:10])}

Numeric Statistics:
{stats}
"""

    return summary
