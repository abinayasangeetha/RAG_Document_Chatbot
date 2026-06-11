def answer_csv_question(
    question,
    csv_dataframes
):

    if not csv_dataframes:
        return None

    # Single CSV

    if len(csv_dataframes) == 1:

        filename = list(
            csv_dataframes.keys()
        )[0]

        df = csv_dataframes[
            filename
        ]

        return execute_query(
            question,
            df,
            filename
        )

    # Multiple CSVs

    lower_question = question.lower()

    for filename, df in (
        csv_dataframes.items()
    ):

        dataset_name = (
            filename
            .replace(".csv", "")
            .lower()
        )

        if dataset_name in lower_question:

            return execute_query(
                question,
                df,
                filename
            )

    # Summarize all datasets

    if (
        "all datasets" in lower_question
        or "all files" in lower_question
    ):

        result = ""

        for filename, df in (
            csv_dataframes.items()
        ):

            result += (
                f"\n{filename}\n"
                f"Rows: {df.shape[0]}\n"
                f"Columns: {df.shape[1]}\n"
            )

        return result

    return (
        "Multiple CSV files uploaded.\n"
        "Please mention dataset name."
    )


from utils.csv_agent import (
    get_csv_instruction
)


def execute_query(
    question,
    df,
    filename
):

    question_lower = question.lower()

    if "rows" in question_lower:

      return (
        f"{filename}\n"
        f"Rows: {df.shape[0]}"
       )

    if "columns" in question_lower:

      return (
        f"{filename}\n"
        f"Columns: {df.shape[1]}"
      )

    if "column names" in question_lower:

      return "\n".join(df.columns)

    if "missing" in question_lower:

      return df.isnull().sum().to_string()

    if (
       "describe" in question_lower
       or "summary" in question_lower
    ):

      return df.describe(
        include="all"
      ).to_string()

    # ADD HERE ↓↓↓

    if (
    "average" in question_lower
    or "mean" in question_lower
):

      matched_columns = []

      for col in df.columns:

        if col.lower() in question_lower:

            matched_columns.append(col)

      if matched_columns:

        col = max(
            matched_columns,
            key=len
        )

        try:

            return (
                f"Average {col}: "
                f"{df[col].mean()}"
            )

        except:

            pass

    if (
    "maximum" in question_lower
    or "max" in question_lower
    or "highest" in question_lower
):

      matched_columns = []

      for col in df.columns:

        if col.lower() in question_lower:

            matched_columns.append(col)

      if matched_columns:

        col = max(
            matched_columns,
            key=len
        )

        try:

            return (
                f"Maximum {col}: "
                f"{df[col].max()}"
            )

        except:

            pass

    if (
    "minimum" in question_lower
    or "min" in question_lower
    or "lowest" in question_lower
):

      matched_columns = []

      for col in df.columns:

        if col.lower() in question_lower:

            matched_columns.append(col)

      if matched_columns:

        col = max(
            matched_columns,
            key=len
        )

        try:

            return (
                f"Minimum {col}: "
                f"{df[col].min()}"
            )

        except:

            pass
    # EXISTING CODE

    instruction = (
        get_csv_instruction(
            question,
            list(df.columns)
        )
    )

    if not instruction:
        return None

    operation = instruction.get(
        "operation"
    )

    if operation in [
    "count_rows",
    "rows",
    "row_count"
         ]:

        return (
            f"{filename}\n"
            f"Rows: {df.shape[0]}"
        )

    if operation in [
    "count_columns",
    "columns",
    "column_count"
        ]:

        return (
            f"{filename}\n"
            f"Columns: {df.shape[1]}"
        )

    if operation == "column_names":

        return (
            f"{filename}\n\n"
            + "\n".join(df.columns)
        )

    if operation == "missing_values":

        return (
            df.isnull()
            .sum()
            .to_string()
        )

    if operation == "describe":

        return (
            df.describe(
                include="all"
            ).to_string()
        )

    if operation in [
    "average",
    "mean"
        ]:

        col = instruction.get(
            "target_column"
        )

        if col in df.columns:

            return (
                f"Average {col}: "
                f"{df[col].mean()}"
            )

    if operation in [
    "maximum",
    "max"
         ]:

        col = instruction.get(
            "target_column"
        )

        if col in df.columns:

            return (
                f"Maximum {col}: "
                f"{df[col].max()}"
            )

    if operation in [
    "minimum",
    "min"
           ]:

        col = instruction.get(
            "target_column"
        )

        if col in df.columns:

            return (
                f"Minimum {col}: "
                f"{df[col].min()}"
            )

    if operation == "lookup":

        target_col = (
            instruction.get(
                "target_column"
            )
        )

        filter_col = (
            instruction.get(
                "filter_column"
            )
        )

        filter_value = (
            instruction.get(
                "filter_value"
            )
        )

        if (
            target_col in df.columns
            and filter_col in df.columns
        ):

            row = df[
                df[filter_col]
                .astype(str)
                ==
                str(filter_value)
            ]

            if not row.empty:

                value = row.iloc[0][
                    target_col
                ]

                return (
                    f"{target_col}: "
                    f"{value}"
                )

    return (
        "Could not answer "
        "from dataset."
    )