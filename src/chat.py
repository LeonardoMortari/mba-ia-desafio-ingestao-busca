from search import search_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def main():
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0
        )
    except Exception as e:
        print("Erro ao inicializar o modelo:", e)
        return

    print("\n💬 Chat iniciado (digite 'sair' para encerrar)\n")

    while True:
        question = input("Pergunta: ")

        if question.lower() == "sair":
            print("Encerrando chat...")
            break

        if not question.strip():
            print("Digite uma pergunta válida.")
            continue

        try:
            prompt = search_prompt(question)

            response = llm.invoke(prompt)

            answer = response.content.strip()

            if not answer:
                answer = "Não tenho informações necessárias para responder sua pergunta."

            print("\nResposta:", answer)

        except Exception as e:
            print("Erro ao processar pergunta:", e)


if __name__ == "__main__":
    main()