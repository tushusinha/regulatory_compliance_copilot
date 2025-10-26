import streamlit as st
import json
import os
import subprocess
import re
from datetime import datetime

# --- File paths ---
OUTPUT_FILE = "./src/data/output/compliance_analysis.json"

# --- Streamlit page config ---
st.set_page_config(
    page_title="Regulatory Compliance Copilot",
    layout="wide",
    page_icon="⚖️"
)

st.title("⚖️ Regulatory Compliance Copilot Dashboard")
st.markdown(
    "An AI-driven assistant that analyses new regulatory updates, maps them to internal policies and controls, and recommends actionable next steps."
)

# --- Refresh button + status bar ---
col1, col2 = st.columns([1, 3])

with col1:
    # --- Refresh Button ---
    if st.button("🔄 Refresh Compliance Data"):
        st.info("Refreshing data... This may take a minute.")
        try:
            # Run the main workflow with FORCE_REFRESH=true
            result = subprocess.run(
                ["python", "src/main.py"],
                env={**os.environ, "FORCE_REFRESH": "true"},
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success("✅ Workflow completed successfully! Data refreshed.")
                st.rerun()
            else:
                st.error("❌ Workflow failed. Check logs.")
                st.code(result.stderr)
        except Exception as e:
            st.error(f"⚠️ Error running refresh: {e}")
with col2:
    # --- Display Last Updated timestamp ---
    if os.path.exists(OUTPUT_FILE):
        timestamp = datetime.fromtimestamp(os.path.getmtime(OUTPUT_FILE))
        st.caption(f"📅 **Last Updated:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.caption("⚠️ No compliance analysis data found. Please refresh to generate results.")

st.markdown("---")

# --- Load and display analysis results ---
if not os.path.exists(OUTPUT_FILE):
    st.warning("No analysis results found. Please run `python main.py` first to generate output.")
    st.stop()

with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    results = json.load(f)

# --- Helper: Clean up Markdown artifacts ---
def clean_markdown(text: str) -> str:
    if not text:
        return ""
    # Remove markdown headers (###, ####, etc.)
    text = re.sub(r"#+\s*", "", text)
    # Remove excessive bold markers
    text = text.replace("**", "")
    # Normalise bullet points
    text = re.sub(r"^\s*-\s*", "• ", text, flags=re.MULTILINE)
    # Fix numbered headings like '1.' or '2.'
    text = re.sub(r"(?m)^\s*(\d+)\.\s*", r"**\1.** ", text)
    # Compact extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

# --- Helper: Color-code priority levels ---
def highlight_priorities(text: str) -> str:
    """Wrap priority keywords in colored HTML spans."""
    if not text:
        return text
    text = re.sub(r"\bHigh\b", r"<span style='color:#e74c3c; font-weight:bold;'>High 🔴</span>", text)
    text = re.sub(r"\bMedium\b", r"<span style='color:#f39c12; font-weight:bold;'>Medium 🟠</span>", text)
    text = re.sub(r"\bLow\b", r"<span style='color:#27ae60; font-weight:bold;'>Low 🟢</span>", text)
    return text

st.subheader("📊 Compliance Analysis Results")

# --- Sidebar ---
st.sidebar.header("Navigation")
tabs = st.sidebar.radio("Choose a view:", ["Regulations", "Mappings", "Impact Analysis", "Recommended Actions"])

# --- Tabs ---
if tabs == "Regulations":
    st.header("📜 New Regulatory Updates")
    for doc in results.get("regulatory_updates", []):
        with st.expander(doc.get("title", "Untitled Regulation"), expanded=False):
            st.write(clean_markdown(doc.get("content", "No content available")))

elif tabs == "Mappings":
    st.header("🗺️ Regulation → Policies & Controls Mapping")
    for m in results.get("mappings", []):
        with st.expander(m.get("regulation_title", "Untitled Regulation"), expanded=False):
            related = m.get("related_policies_controls", [])
            if not related:
                st.write("_No mappings found._")
            else:
                for r in related:
                    st.markdown(f"• {clean_markdown(r['text'])}")
                    if r.get("metadata"):
                        st.caption(f"Source: {r['metadata'].get('type', 'N/A')}")

elif tabs == "Impact Analysis":
    st.header("🔍 Impact Summaries")
    for impact in results.get("impacts", []):
        with st.expander(impact.get("regulation_title", "Untitled Regulation"), expanded=False):
            st.text_area("Impact Analysis", clean_markdown(impact.get("impact_analysis", "")), height=250)

elif tabs == "Recommended Actions":
    st.header("🧭 Compliance Recommendations")
    for action in results.get("actions", []):
        with st.expander(action.get("regulation_title", "Untitled Regulation"), expanded=False):
            clean_text = clean_markdown(action.get("recommended_actions", ""))
            highlighted = highlight_priorities(clean_text)
            # Render as HTML for colored spans
            st.markdown(highlighted, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.caption("Developed as a Proof of Concept – Regulatory Compliance Copilot © 2025")
