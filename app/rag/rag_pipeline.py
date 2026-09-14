from app.rag.ingestion import extract_text, chunk_text
from app.rag.retriever import retrieve
from app.rag.reranker import reranker
from app.llm.qwen import generate_response


def run_rag(query, file_path):

    text = extract_text(file_path)

    chunks = chunk_text(text)

    documents = retrieve(
        query,
        chunks,
        top_k=3
    )

    context = reranker(
        query,
        documents,
        top_k=3
    )

    answer = generate_response(
        query,
        context
    )

    return answer