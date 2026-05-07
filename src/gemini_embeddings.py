import time
import google.generativeai as genai
from langchain_core.embeddings import Embeddings

class GeminiEmbeddings(Embeddings):
    def __init__(
        self,
        model="models/gemini-embedding-001",
        delay=1.5
    ):
        self.model = model
        self.delay = delay

    def embed_documents(self, texts):
        embeddings = []

        for index, text in enumerate(texts):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text
                )

                embeddings.append(result["embedding"])

                print(f"Embedding {index + 1}/{len(texts)} criado")

            except Exception as e:
                print(f"Erro ao criar embedding: {e}")
                raise e

        return embeddings

    def embed_query(self, text):
        result = genai.embed_content(
            model=self.model,
            content=text
        )

        return result["embedding"]