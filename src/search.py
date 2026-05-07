import os
from dotenv import load_dotenv
from pathlib import Path

import google.generativeai as genai

from langchain_postgres import PGVector
from gemini_embeddings import GeminiEmbeddings

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DB_CONNECTION = os.getenv("DATABASE_URL")
COLLECTION_NAME = "pdf_docs"


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def create_vectorstore():
    embeddings = GeminiEmbeddings()

    return PGVector(
        embeddings=embeddings,
        connection=DB_CONNECTION,
        collection_name=COLLECTION_NAME
    )


def search_documents(question: str, k=10):
    vectorstore = create_vectorstore()

    results = vectorstore.similarity_search_with_score(question, k=k)

    return results


def build_context(results):
    results = results[:5]

    return "\n\n".join([doc.page_content for doc, _ in results])


def search_prompt(question=None):
    if not question:
        raise ValueError("Pergunta não pode ser vazia")

    results = search_documents(question)

    context = build_context(results)

    if not context.strip():
        return PROMPT_TEMPLATE.format(
            contexto="",
            pergunta=question
        )

    prompt = PROMPT_TEMPLATE.format(
        contexto=context,
        pergunta=question
    )

    return prompt