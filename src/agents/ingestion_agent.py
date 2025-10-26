"""
Regulation Ingestion Agent
Fetches, processes, summarizes, and caches FCA/PRA regulatory updates.
"""

import os
import json
from loguru import logger
from bs4 import BeautifulSoup
import requests


class IngestionAgent:
    def __init__(self, llm_client, retriever, mode="mock", force_refresh=False):
        self.llm_client = llm_client
        self.retriever = retriever
        self.mode = mode
        self.force_refresh = force_refresh
        self.source_urls = [
            "https://www.fca.org.uk/news",
            "https://www.bankofengland.co.uk/prudential-regulation/publication/2024/july/pra-annual-report-2023-24"
        ]

        # ✅ Cache file location
        self.cache_file = "./src/data/output/summarized_regulations.json"

    def fetch_latest_updates(self):
        """Fetch, summarize, and store the latest regulatory updates."""
        logger.info(f"📥 Starting ingestion in mode: {self.mode}")

        # ✅ Skip cache if forced
        if not self.force_refresh:
            # ✅ Load from cache if available
            cached_docs = self._load_from_cache()
            if cached_docs:
                logger.info(f"💾 Loaded {len(cached_docs)} summarized documents from cache.")
                return cached_docs
            else:
                logger.info("⚠️ No valid cache found — fetching new data.")
        else:
            logger.info("♻️ Force refresh enabled — skipping cache.")

        # Otherwise fetch fresh data
        if self.mode == "live":
            raw_docs = self._fetch_from_web()
        else:
            raw_docs = self._fetch_from_local()

        if not raw_docs:
            logger.warning("No new regulatory documents found.")
            return []

        summarized_docs = []

        # ✅ Summarize each document using the LLM
        for doc in raw_docs:
            title = doc.get("title", "Untitled Regulation")
            content = doc.get("content", title)  # fallback if only title is available
            doc_id = doc.get("id", f"doc_{hash(title)}")
            source = doc.get("source", "Unknown")

            try:
                logger.info(f"🧾 Summarizing document: {title[:60]}...")

                summary = self.llm_client.summarize_text(
                    content,
                    max_length=250
                )

                summarized_doc = {
                    "id": doc_id,
                    "regulation_title": title,
                    "regulation_text": summary,
                    "title": title,
                    "content": summary,
                    "source": source
                }

                summarized_docs.append(summarized_doc)
                # Optionally, store summarized version in retriever
                self.retriever.add_document(doc_id, summary, {"source": source})

            except Exception as e:
                logger.error(f"❌ Error summarizing {title}: {e}")
                summarized_docs.append({
                    "id": doc_id,
                    "regulation_title": title,
                    "regulation_text": "Error summarizing document.",
                    "source": source
                })

        # ✅ Save summarized results to cache
        self._save_to_cache(summarized_docs)

        logger.info(f"✅ Successfully summarized and cached {len(summarized_docs)} documents.")
        return summarized_docs

    # ---------------------------
    # Internal fetchers
    # ---------------------------

    def _fetch_from_local(self):
        """Read mock documents from local folder."""
        base_dir = "./src/data/regulatory_updates"
        new_docs = []

        for file in os.listdir(base_dir):
            if file.endswith(".txt"):
                file_path = os.path.join(base_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                doc_id = f"mock_{file}"
                self.retriever.add_document(doc_id, content, {"source": "local"})
                new_docs.append({
                    "id": doc_id,
                    "title": file.replace(".txt", ""),
                    "content": content,
                    "source": "local"
                })

        logger.info(f"📄 Fetched {len(new_docs)} mock documents from local folder.")
        return new_docs

    def _fetch_from_web(self):
        """Fetch and process live FCA/PRA updates."""
        new_docs = []

        for url in self.source_urls:
            try:
                res = requests.get(url, timeout=10)
                soup = BeautifulSoup(res.text, "html.parser")

                # Extract some visible text or headlines
                titles = [a.text.strip() for a in soup.find_all("a") if a.text.strip()]
                for t in titles[:3]:  # limit to 3 per source
                    doc_id = f"doc_{hash(t)}"
                    self.retriever.add_document(doc_id, t, {"source": url})
                    new_docs.append({
                        "id": doc_id,
                        "title": t,
                        "content": t,  # Use title as fallback content
                        "source": url
                    })

            except Exception as e:
                logger.error(f"⚠️ Error fetching from {url}: {e}")

        logger.info(f"🌐 Fetched {len(new_docs)} live documents from the web.")
        return new_docs

    # ------------------------------------------------------------------
    # Cache utilities
    # ------------------------------------------------------------------
    def _load_from_cache(self):
        """Load summarized docs if cache file exists."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except Exception as e:
                logger.error(f"⚠️ Error reading cache file: {e}")
        return None

    def _save_to_cache(self, summarized_docs):
        """Persist summarized documents to JSON cache."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(summarized_docs, f, indent=2)
            logger.info(f"💾 Saved summarized docs to cache: {self.cache_file}")
        except Exception as e:
            logger.error(f"⚠️ Error saving cache: {e}")
