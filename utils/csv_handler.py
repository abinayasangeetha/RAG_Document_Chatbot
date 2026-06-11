import pandas as pd

csv_dataframes = {}


def store_csv(
    filename,
    file_path
):

    df = pd.read_csv(file_path)

    csv_dataframes[
        filename
    ] = df

    return df