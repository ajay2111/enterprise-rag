from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def reranker(query, documents,  top_k=3):

    pairs = [
        [query, document] 
        for document in documents
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x : x[1],
        reverse=True
    )

    return [
        documents
        for document, scores in ranked[:top_k]
    ]