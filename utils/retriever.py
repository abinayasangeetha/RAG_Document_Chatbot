def retrieve_context(
    vectorstore,
    question,
    k=20
):

    docs1 = vectorstore.similarity_search(
        question,
        k=15
    )

    docs2 = vectorstore.max_marginal_relevance_search(
        question,
        k=15,
        fetch_k=40
    )

    combined = []

    seen = set()

    for doc in docs1 + docs2:

        text = doc.page_content

        if text not in seen:

            seen.add(text)

            combined.append(doc)

    context = "\n\n".join(
        [
            doc.page_content
            for doc in combined
        ]
    )

    return context, combined