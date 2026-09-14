from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from app.rag.ingestion import client, embed_query, get_context

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_query(query):
    return model.encode(query).tolist()


def bm25_search(query, documents, top_k=3):

    tokenized_documents = [
        document.split()
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    query_tokens = query.split()

    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        document
        for document, scores in ranked[:top_k]
    ]

def rrf(vector_results, bm25_results, top_k=3):

    scores = {}

    for rank, document in enumerate(vector_results):
        scores[document] = scores.get(document, 0) + 1 / ( 60 + rank + 1)

    for rank, document in enumerate(bm25_results):
            scores[document] = scores.get(document, 0) + 1 / ( 60 + rank + 1)

    ranked = sorted(scores.items(), key=lambda x : x[1], reverse=True)

    return [document for document, score in ranked[:top_k]]

def retreiver(query, documents, top_k=3):

    query_vector = embed_query(query)

    results = client.query_points(
        collection_name = "documents"
        query=query_vector,
        limit=10
    )

    vector_results = get_context(results)

    bm25_results = bm25_search(query, documents, top_k=10)

    return rrf(
        vector_results,
        bm25_results,
        top_k=top_k         
    )
     

def get_context(results):
    return [
        point.payload["text"]
        for point in results.points
    ]