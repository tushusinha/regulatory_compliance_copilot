from loguru import logger


class MappingAgent:
    """
    MappingAgent:
    Uses semantic search (via Retriever) to identify which internal policies
    and controls relate to new or updated regulations.
    """

    def __init__(self, llm_client, retriever):
        self.llm_client = llm_client
        self.retriever = retriever

    def map_to_policies_and_controls(self, regulatory_docs):
        """Map each new regulation to potentially related policies and controls."""
        logger.info("🗺️ Mapping new regulations to internal policies and controls...")

        mappings = []

        for doc in regulatory_docs:
            title = doc.get("title", "Untitled Regulation")
            content = doc.get("content", "")

            query = f"Find internal policies and controls related to this regulation: {title}\n\n{content}"

            # Semantic search against stored internal docs
            results = self.retriever.search(query, top_k=5)

            # Simplify structure for downstream agents
            related_items = []
            if results and "documents" in results:
                for i, doc_text in enumerate(results["documents"][0]):
                    meta = results["metadatas"][0][i] if "metadatas" in results else {}
                    related_items.append({"text": doc_text, "metadata": meta})

            mappings.append({
                "regulation_title": title,
                "regulation_text": content,
                "related_policies_controls": related_items
            })

        logger.success(f"✅ Completed mapping for {len(mappings)} regulatory updates.")
        return mappings
