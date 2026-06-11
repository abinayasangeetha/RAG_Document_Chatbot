def is_csv_query(question):

    question = question.lower()

    keywords = [

        "row",
        "rows",

        "column",
        "columns",

        "average",
        "mean",

        "maximum",
        "minimum",

        "highest",
        "lowest",

        "describe",
        "summary",

        "dataset",

        "missing",

        "customer",
        "employee",
        "student",

        "trip",
        "price",
        "salary",
        "income",

        "id"
    ]

    return any(
        keyword in question
        for keyword in keywords
    )