from loguru import logger


class ActionAgent:
    """
    ActionAgent:
    Translates impact analysis into actionable next steps for compliance teams.
    """

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate_recommendations(self, impact_summary):
        """Generate prioritized compliance actions based on the impact summary."""
        title = impact_summary.get("regulation_title", "Unknown Regulation")
        logger.info(f"🧭 Generating recommendations for: {title}")

        impact_text = impact_summary.get("impact_analysis", "No impact summary provided.")

        prompt = f"""
You are a senior compliance officer at a UK financial institution.
Based on the following impact analysis, propose specific, practical actions
the compliance and operations teams should take.

Impact Analysis:
{impact_text}

Provide output as a clear action plan with the following sections:
1. Action Item
2. Priority (High / Medium / Low)
3. Responsible Owner or Department
4. Target Completion Timeline
5. Rationale
"""

        try:
            # ✅ Correct method call
            result_text = self.llm_client.generate_text(prompt)

            if not result_text or "Error" in result_text:
                raise ValueError("Invalid or empty LLM response")

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            result_text = "Error generating recommendations."

        return {
            "regulation_title": title,
            "recommended_actions": result_text
        }
