from pathlib import Path


def load_knowledge_base(data_folder: str = "data") -> str:
    data_path = Path(data_folder)
    texts = []

    for file_path in data_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        texts.append(f"\n\n--- Source: {file_path.name} ---\n{content}")

    return "\n".join(texts)
