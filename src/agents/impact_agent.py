from loguru import logger


class ImpactAgent:
    """
    ImpactAgent:
    Compares regulatory updates against mapped policies/controls to
    identify possible compliance gaps and business impacts.
    """

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def evaluate_impact(self, mapping):
        """Assess how a regulatory change affects existing internal controls/policies."""
        logger.info(f"🔍 Evaluating impact for regulation: {mapping['regulation_title']}")

        regulation_text = mapping.get("regulation_text", "")
        related_items = mapping.get("related_policies_controls", [])

        # Build concise context for LLM
        context = "\n".join([f"- {item['text']}" for item in related_items]) or "No related policies found."

        # Build a domain-specific prompt
        prompt = f"""
You are a senior compliance expert at a UK bank.
Analyze how the following new regulation impacts internal policies and controls.

Regulation:
{regulation_text}

Related Internal Policies & Controls:
{context}

Provide the output in three clear sections:
1. Impact Summary
2. Identified Gaps
3. Recommended Focus Areas
"""

        try:
            # ✅ Corrected call — use the actual method in LLMClient
            result_text = self.llm_client.generate_text(prompt)

            if not result_text or "Error" in result_text:
                raise ValueError("Invalid or empty LLM response")

        except Exception as e:
            logger.error(f"Error generating impact summary: {e}")
            result_text = "Error generating impact summary."

        return {
            "regulation_title": mapping.get("regulation_title", "Unknown Regulation"),
            "impact_analysis": result_text
        }
