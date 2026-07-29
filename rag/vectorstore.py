import os
from langchain_community.vectorstores import FAISS

from rag.embeddings import get_embedding_model


VECTOR_DB = "vector_db"


def build_vector_store(chunks):

    embeddings = get_embedding_model()

    db = FAISS.from_documents(

        chunks,

        embeddings,
    )

    os.makedirs(VECTOR_DB, exist_ok=True)

    db.save_local(VECTOR_DB)

    return db


def load_vector_store():

    embeddings = get_embedding_model()

    return FAISS.load_local(

        VECTOR_DB,

        embeddings,

        allow_dangerous_deserialization=True,
    )