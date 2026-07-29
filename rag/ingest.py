from rag.loader import load_documents
from rag.splitter import split_documents
from rag.vectorstore import build_vector_store


def main():

    print("Loading documents...")

    docs = load_documents()

    print(f"Loaded {len(docs)} documents.")

    print("Splitting...")

    chunks = split_documents(docs)

    print(f"Generated {len(chunks)} chunks.")

    print("Building FAISS index...")

    build_vector_store(chunks)

    print("Done!")

    print("Vector database saved to vector_db/")


if __name__ == "__main__":
    main()