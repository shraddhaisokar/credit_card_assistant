import os
import uuid
from backend.chunker import chunk_text
from backend.embedder import embed_texts, embed_query
from backend.vector_store import VectorStore
from backend.intent_classifier import classify_intent
from backend.mock_api import MockAPI
from backend.generator import Generator
from backend.document_loader import load_text_from_file


class CreditCardAssistant:
    def __init__(self, docs_folder="docs"):
        self.history = []

        print("Loading documents...")
        docs = []

        for filename in os.listdir(docs_folder):
            path = os.path.join(docs_folder, filename)
            if not os.path.isfile(path):
                continue

            text = load_text_from_file(path)
            chunks = chunk_text(text)

            for chunk in chunks:
                docs.append({
                    "id": str(uuid.uuid4()),
                    "source": filename,
                    "text": chunk
                })

        print("Embedding...")
        embeddings = embed_texts([d["text"] for d in docs])
        self.store = VectorStore(docs, embeddings)

        self.api = MockAPI()
        self.generator = Generator()

    def handle(self, query):
        self.history.append({"role": "user", "text": query})

        intent = classify_intent(query)

        if intent != "informational":
            reply = self.api.call(intent)
            self.history.append({"role": "bot", "text": reply})
            return reply

        q_vec = embed_query(query)
        docs = self.store.search(q_vec)

        context = "\n".join([d["text"] for d in docs])
        reply = self.generator.answer(query, context, self.history)
        self.history.append({"role": "bot", "text": reply})

        return reply
