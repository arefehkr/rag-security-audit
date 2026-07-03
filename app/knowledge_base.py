"""
Builds and loads the vector store that backs the RAG app.

Uses a local sentence-transformers embedding model (no API key needed) and
Chroma as the vector store. Swap in OpenAI embeddings if you prefer -- see
the commented alternative below.
"""

import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_store")


def build_vectorstore(persist: bool = True):
    """Load documents/*.txt, chunk them, embed, and store in Chroma."""
    loader = DirectoryLoader(DOCS_DIR, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=PERSIST_DIR if persist else None,
    )
    if persist:
        vectordb.persist()
    return vectordb


def load_vectorstore():
    """Load a previously-built vector store from disk."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)


if __name__ == "__main__":
    # Run this directly to (re)build the index after editing documents/*.txt
    build_vectorstore()
    print(f"Vector store built and persisted to {PERSIST_DIR}")
