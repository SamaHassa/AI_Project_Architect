from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model

DB_PATH = "vector_db"


def retrieve_context(query: str, k: int = 5):
    """
    Retrieve the most relevant documentation
    from the FAISS vector database.
    """

    embeddings = get_embedding_model()

    vector_store = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    docs = vector_store.similarity_search(
        query,
        k=k,
    )

    return docs