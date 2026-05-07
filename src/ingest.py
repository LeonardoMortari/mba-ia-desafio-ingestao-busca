import os
from dotenv import load_dotenv
from pathlib import Path

import google.generativeai as genai

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from gemini_embeddings import GeminiEmbeddings

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env"
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DB_CONNECTION = os.getenv("DATABASE_URL")
COLLECTION_NAME = "pdf_docs"

def load_pdf():
    loader = PyPDFLoader("document.pdf")
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    return splitter.split_documents(documents)


def create_embeddings():
    return GeminiEmbeddings()


def create_vectorstore(embeddings):
    return PGVector(
        embeddings=embeddings,
        connection=DB_CONNECTION,
        collection_name=COLLECTION_NAME
    )


def store_documents(vectorstore, chunks):
    for index, chunk in enumerate(chunks):
        print(f"Salvando chunk {index + 1}/{len(chunks)}")

        vectorstore.add_documents([chunk])


def ingest_pdf():
    print("📄 Carregando PDF...")
    docs = load_pdf()

    print("✂️ Dividindo em chunks...")
    chunks = split_documents(docs)

    print(f"📦 Total de chunks: {len(chunks)}")

    print("🧠 Criando embeddings...")
    embeddings = create_embeddings()

    print("💾 Conectando ao banco...")
    vectorstore = create_vectorstore(embeddings)

    print("🚀 Salvando no banco...")
    store_documents(vectorstore, chunks)

    print("✅ Ingestão concluída!")


if __name__ == "__main__":
    ingest_pdf()