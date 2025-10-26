"""
Regulatory Compliance Copilot - Main Entry Point
Author: Baxi Sinha
Description:
    This PoC demonstrates an Agentic AI system that autonomously reads FCA/PRA
    regulatory updates, maps them to internal policies, and suggests compliance actions.
"""

import os
from dotenv import load_dotenv
import yaml
from loguru import logger

# Import internal modules
from core.llm_client import LLMClient
from core.retriever import Retriever
from orchestration.workflow import Workflow
from utils.logger import init_logger
from agents.ingestion_agent import IngestionAgent


def load_config():
    """Load YAML configuration and environment variables."""
    load_dotenv()
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "settings.yaml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def initialize_system(config):
    """Initialize all major components."""
    logger.info("Initializing Regulatory Compliance Copilot...")

    # Initialize core LLM client
    llm_client = LLMClient(
        model_name=os.getenv("MODEL_NAME", "gpt-4o"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Initialize Retriever (RAG pipeline)
    retriever = Retriever(
        vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/embeddings"),
        embedding_model=config["models"]["embedding_model"]
    )

    retriever.load_from_directory("./src/data/policies", "policy")
    retriever.load_from_directory("./src/data/regulatory_updates", "regulation")
    retriever.load_controls_from_directory("./src/data/controls")

    # Read from .env (default: false)
    force_refresh = os.getenv("FORCE_REFRESH", "false").lower() == "true"

    # Initialize ingestion agent
    ingestion_agent = IngestionAgent(
        llm_client=llm_client,
        retriever=retriever,
        mode="mock",
        force_refresh=force_refresh
    )

    # Initialize Orchestration Workflow
    workflow = Workflow(
        llm_client=llm_client,
        retriever=retriever,
    ingestion_agent=ingestion_agent
    )

    return workflow


def main():
    """Main execution flow."""
    init_logger()
    config = load_config()
    workflow = initialize_system(config)

    logger.info("System initialized successfully ✅")

    # Run the workflow
    workflow.run()


if __name__ == "__main__":
    main()
