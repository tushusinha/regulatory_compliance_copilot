import json
from loguru import logger

from agents.ingestion_agent import IngestionAgent
from agents.mapping_agent import MappingAgent
from agents.impact_agent import ImpactAgent
from agents.action_agent import ActionAgent


class Workflow:
    """
    Orchestrates the full multi-agent regulatory compliance pipeline:
    1️⃣ Ingest new regulatory data
    2️⃣ Map to internal policies and controls
    3️⃣ Assess compliance impact
    4️⃣ Recommend actions
    """

    def __init__(self, llm_client, retriever, ingestion_agent=None):
        self.llm_client = llm_client
        self.retriever = retriever
        self.ingestion_agent = ingestion_agent or IngestionAgent(llm_client, retriever, mode="mock")

        # Initialize downstream agents
        self.mapping_agent = MappingAgent(llm_client, retriever)
        self.impact_agent = ImpactAgent(llm_client)
        self.action_agent = ActionAgent(llm_client)

    def run(self):
        """Run the complete regulatory compliance analysis workflow."""
        logger.info("🚀 Starting Regulatory Compliance Copilot workflow...")

        # --- 1️⃣ Ingest new regulations ---
        logger.info("Step 1: Ingesting latest regulatory updates...")
        new_docs = self.ingestion_agent.fetch_latest_updates()
        print("DEBUG DOCS:", new_docs)

        if not new_docs:
            logger.warning("No new regulatory documents found. Exiting workflow.")
            return

        logger.info(f"Fetched {len(new_docs)} new regulatory updates.")
        logger.debug(json.dumps(new_docs, indent=2))

        # --- 2️⃣ Map to internal policies & controls ---
        logger.info("Step 2: Mapping regulations to internal policies and controls...")
        mappings = self.mapping_agent.map_to_policies_and_controls(new_docs)
        logger.info(f"Generated {len(mappings)} mappings.")
        logger.debug(json.dumps(mappings, indent=2))

        # --- 3️⃣ Assess impact ---
        logger.info("Step 3: Assessing impact for each regulatory update...")
        impact_summaries = []
        for mapping in mappings:
            impact = self.impact_agent.evaluate_impact(mapping)
            impact_summaries.append(impact)

        logger.info(f"Completed impact analysis for {len(impact_summaries)} regulations.")
        logger.debug(json.dumps(impact_summaries, indent=2))

        # --- 4️⃣ Recommend compliance actions ---
        logger.info("Step 4: Generating recommended actions...")
        actions = []
        for impact in impact_summaries:
            action_plan = self.action_agent.generate_recommendations(impact)
            actions.append(action_plan)

        logger.info(f"Generated {len(actions)} action plans.")
        logger.debug(json.dumps(actions, indent=2))

        # --- ✅ Final Output ---
        results = {
            "regulatory_updates": new_docs,
            "mappings": mappings,
            "impacts": impact_summaries,
            "actions": actions
        }

        output_path = "./src/data/output/compliance_analysis.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        logger.success(f"🎯 Workflow completed successfully! Results saved to: {output_path}")

        return results
