"""
Retriever Module
Handles document embedding, vector search, and retrieval (RAG pipeline).
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger

import json


class Retriever:
    def __init__(self, vector_db_path: str, embedding_model: str):
        self.vector_db_path = vector_db_path
        self.embedding_model_name = embedding_model
        self.documents = {}  # mock in-memory store

        logger.info(f"Initializing retriever with model: {embedding_model}")
        self.model = SentenceTransformer(embedding_model)

        self.client = chromadb.PersistentClient(
            path=vector_db_path,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection("regulatory_docs")

    def add_document(self, doc_id: str, text: str, metadata: dict = None):
        """Embed and add document to vector DB."""
        embedding = self.model.encode([text])[0].tolist()
        self.collection.add(ids=[doc_id], embeddings=[embedding], documents=[text], metadatas=[metadata or {}])
        logger.debug(f"Document added to vector DB: {doc_id}")

    def search(self, query: str, top_k: int = 3):
        """Semantic search for most relevant documents."""
        query_embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results

    def load_from_directory(self, directory, doc_type):
        """Load mock text files from a folder (e.g., data/policies/)."""
        logger.info(f"Loading {doc_type} documents from {directory}...")
        for file_name in os.listdir(directory):
            if file_name.endswith(".txt"):
                with open(os.path.join(directory, file_name), "r", encoding="utf-8") as f:
                    content = f.read()
                    doc_id = f"{doc_type}_{file_name}"
                    self.add_document(doc_id, content, {"type": doc_type})
        logger.info(f"Loaded {len(self.documents)} {doc_type} documents.")

    def load_controls_from_directory(self, directory):
        """Load JSON files containing internal control data."""
        import os
        from loguru import logger

        logger.info(f"Loading internal controls from {directory}...")
        for file in os.listdir(directory):
            if file.endswith(".json"):
                with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
                    controls = json.load(f)
                    for ctrl in controls:
                        doc_id = f"control_{ctrl['control_id']}"
                        text = f"{ctrl['name']}: {ctrl['description']}"
                        self.add_document(doc_id, text, {"type": "control", "owner": ctrl["owner"]})
        logger.info(f"Loaded {len(self.documents)} total documents after adding controls.")

