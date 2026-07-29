from langchain_community.document_loaders import DirectoryLoader, TextLoader


DATA_PATH = "data/knowledge_base"


def load_documents():

    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True,
        },
        show_progress=True,
        use_multithreading=True,
        silent_errors=True,
    )

    documents = loader.load()

    return documents