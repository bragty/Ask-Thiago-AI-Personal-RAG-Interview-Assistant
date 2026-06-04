import json
from pathlib import Path
from typing import Any

import numpy as np

from src.config import get_openai_client


EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_DATA_DIR = "data"
DEFAULT_INDEX_PATH = "vector_index/index.json"


def load_markdown_files(data_dir: str = DEFAULT_DATA_DIR) -> list[dict[str, str]]:
    data_path = Path(data_dir)
    documents: list[dict[str, str]] = []

    for file_path in sorted(data_path.glob("*.md")):
        documents.append(
            {
                "source": file_path.name,
                "text": file_path.read_text(encoding="utf-8"),
            }
        )

    return documents


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    """Split long text into overlapping chunks so retrieval keeps nearby context."""
    cleaned_text = " ".join(text.split())
    if not cleaned_text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(cleaned_text):
        end = start + chunk_size
        chunks.append(cleaned_text[start:end])

        if end >= len(cleaned_text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def build_chunks(data_dir: str = DEFAULT_DATA_DIR) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []

    for document in load_markdown_files(data_dir):
        for index, chunk in enumerate(chunk_text(document["text"])):
            chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": f"{document['source']}::chunk_{index}",
                    "text": chunk,
                }
            )

    return chunks


def create_embedding(text: str) -> list[float]:
    """Create an OpenAI embedding vector used for semantic search."""
    client = get_openai_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Measure how similar two embedding vectors are by comparing their direction."""
    a = np.array(vector_a, dtype=np.float32)
    b = np.array(vector_b, dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def build_vector_index(chunks: list[dict[str, str]]) -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []

    for chunk in chunks:
        index.append(
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "embedding": create_embedding(chunk["text"]),
            }
        )

    return index


def retrieve_relevant_chunks(
    question: str,
    vector_index: list[dict[str, Any]],
    top_k: int = 5,
) -> list[dict[str, Any]]:
    question_embedding = create_embedding(question)
    scored_chunks: list[dict[str, Any]] = []

    for item in vector_index:
        similarity = cosine_similarity(question_embedding, item["embedding"])
        scored_chunks.append({**item, "similarity": similarity})

    return sorted(scored_chunks, key=lambda chunk: chunk["similarity"], reverse=True)[:top_k]


def format_chunks_for_prompt(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return "No relevant context was retrieved from the knowledge base."

    formatted_chunks = []
    for chunk in chunks:
        formatted_chunks.append(
            "\n".join(
                [
                    f"Source: {chunk['source']}",
                    f"Chunk ID: {chunk['chunk_id']}",
                    f"Similarity: {chunk.get('similarity', 0.0):.3f}",
                    chunk["text"],
                ]
            )
        )

    return "\n\n---\n\n".join(formatted_chunks)


def save_vector_index(
    index: list[dict[str, Any]],
    output_path: str = DEFAULT_INDEX_PATH,
) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(index, indent=2), encoding="utf-8")


def load_saved_vector_index(index_path: str = DEFAULT_INDEX_PATH) -> list[dict[str, Any]]:
    index_file = Path(index_path)
    if not index_file.exists():
        raise FileNotFoundError(f"Vector index not found at {index_file}")

    return json.loads(index_file.read_text(encoding="utf-8"))


def get_or_build_vector_index(
    data_dir: str = DEFAULT_DATA_DIR,
    index_path: str = DEFAULT_INDEX_PATH,
) -> list[dict[str, Any]]:
    """Load saved embeddings when available; otherwise build them dynamically."""
    if Path(index_path).exists():
        return load_saved_vector_index(index_path)

    chunks = build_chunks(data_dir=data_dir)
    return build_vector_index(chunks)
