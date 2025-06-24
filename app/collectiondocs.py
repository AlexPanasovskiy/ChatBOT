import chromadb
import json
from chromadb.utils import embedding_functions


client = chromadb.Client()
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "paraphrase-multilingual-MiniLM-L12-v2")
collection = client.create_collection(name = "anylogicdocs",
                                      embedding_function = embedding_func)


with open('app/docs/anylogicdocs.json') as f:
    data = json.load(f)
    collection.add(
        documents = [f"Вопрос: {q['question']}\nОтвет: {q['answer']}" for q in data],
        metadatas = [q["metadata"] for q in data],
        ids = [q["id"] for q in data])