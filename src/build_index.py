from src.rag import DEFAULT_DATA_DIR, DEFAULT_INDEX_PATH, build_chunks, build_vector_index, save_vector_index


def main() -> None:
    print("Loading markdown files...")
    chunks = build_chunks(data_dir=DEFAULT_DATA_DIR)
    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings...")
    vector_index = build_vector_index(chunks)

    save_vector_index(vector_index, output_path=DEFAULT_INDEX_PATH)
    print(f"Saved vector index to {DEFAULT_INDEX_PATH}.")


if __name__ == "__main__":
    main()
