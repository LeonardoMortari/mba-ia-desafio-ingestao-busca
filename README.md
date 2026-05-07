# Desafio Técnico — RAG com LangChain + Gemini + pgVector

Este projeto implementa um sistema de RAG (Retrieval-Augmented Generation) utilizando:

- Python
- LangChain
- Google Gemini
- PostgreSQL + pgVector
- Docker / Docker Compose

A aplicação realiza:

- ingestão de um arquivo PDF
- geração de embeddings
- armazenamento vetorial no PostgreSQL
- busca semântica
- interação via CLI

---

# 📁 Estrutura do Projeto

```bash
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
├── README.md
└── src/
    ├── ingest.py
    ├── search.py
    ├── chat.py
    └── gemini_embeddings.py
```

---

# 🚀 Tecnologias Utilizadas

- Python 3.11
- LangChain
- Google Gemini API
- PostgreSQL
- pgVector
- Docker

---

# ⚙️ Pré-requisitos

Antes de executar o projeto, instale:

- Docker
- Docker Compose
- Python 3.11
- pip
- virtualenv

---

# 🔑 Configuração da API Key

Crie uma API Key no Google AI Studio:

https://aistudio.google.com/app/apikey

---

# 📄 Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_api_key_aqui

DB_CONNECTION=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres
```

---

# 🐳 Como Executar o Projeto

## 1. Clone o repositório

```bash
git clone <url-do-repositorio>

cd mba-ia-desafio-ingestao-busca
```

---

## 2. Suba o banco PostgreSQL com pgVector

```bash
docker compose up -d
```

Verifique se o container está rodando:

```bash
docker ps
```

---

## 3. Crie o ambiente virtual

### Linux / MacOS

```bash
python3.11 -m venv venv
```

---

## 4. Ative o ambiente virtual

```bash
source venv/bin/activate
```

---

## 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 6. Configure o arquivo `.env`

Crie o arquivo `.env` na raiz do projeto:

```env
GOOGLE_API_KEY=sua_api_key_aqui

DB_CONNECTION=postgresql+psycopg2://postgres:postgres@localhost:5432/postgres
```

---

## 7. Adicione o PDF

Coloque o arquivo PDF na raiz do projeto com o nome:

```bash
document.pdf
```

---

## 8. Execute a ingestão

```bash
python src/ingest.py
```

Exemplo de saída:

```bash
📄 Carregando PDF...
✂️ Dividindo em chunks...
🧠 Criando embeddings...
💾 Conectando ao banco...
🚀 Salvando no banco...
✅ Ingestão concluída!
```

---

## 9. Execute o chat

```bash
python src/chat.py
```

---

# 💬 Exemplo de uso

```bash
Pergunta: Qual o faturamento da empresa?

Resposta:
O faturamento da empresa foi de 10 milhões de reais.
```

---

# ❌ Perguntas fora do contexto

```bash
Pergunta: Qual é a capital da França?

Resposta:
Não tenho informações necessárias para responder sua pergunta.
```

---

# 🧠 Funcionamento da Aplicação

## Fluxo da ingestão

1. Leitura do PDF
2. Divisão em chunks
3. Geração de embeddings
4. Armazenamento no PostgreSQL com pgVector

---

## Fluxo da busca

1. Usuário envia pergunta via CLI
2. Pergunta é convertida em embedding
3. Busca semântica no banco vetorial
4. Construção do prompt com contexto
5. Chamada do Gemini
6. Retorno da resposta

---

# 🔥 Configuração dos chunks

O projeto utiliza:

```python
chunk_size=1000
chunk_overlap=150
```

Esses valores foram ajustados para reduzir chamadas no plano gratuito do Gemini.

---

# ⚠️ Observações importantes

- O plano gratuito do Gemini possui limite de requisições.
- Durante os testes, a ingestão foi limitada para evitar erro `429 RESOURCE_EXHAUSTED`.
- Após a ingestão do PDF, não é necessário executar novamente o `ingest.py`, exceto em caso de alteração do documento.

---

# 🧹 Limpando embeddings do banco

Caso queira reiniciar a ingestão:

```sql
DELETE FROM langchain_pg_embedding;
```