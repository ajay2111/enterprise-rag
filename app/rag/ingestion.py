import fitz

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


client = QdrantClient(":memory:")

model = SentenceTransformer("all-MiniLM-L6-v2")


client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)


def extract_text(file_path):

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    return text


def chunk_text(text, chunk_size=1000):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def create_embeddings(chunks):

    return model.encode(chunks)


def database(chunks, embeddings):

    points = [
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={"text": chunk}
        )
        for i, (chunk, embedding)
        in enumerate(zip(chunks, embeddings))
    ]

    client.upsert(
        collection_name="documents",
        points=points
    )