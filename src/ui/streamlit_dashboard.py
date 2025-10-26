import streamlit as st
import json
import os

OUTPUT_PATH = "./src/data/output/compliance_analysis.json"

st.set_page_config(
    page_title="Regulatory Compliance Copilot",
    layout="wide",
    page_icon="⚖️"
)

st.title("⚖️ Regulatory Compliance Copilot Dashboard")
st.markdown(
    "An AI-driven assistant that analyzes new regulatory updates, maps them to internal policies and controls, and recommends actionable next steps."
)

# --- Load Results ---
if not os.path.exists(OUTPUT_PATH):
    st.warning("No analysis results found. Please run `python main.py` first to generate output.")
    st.stop()

with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
    results = json.load(f)

# --- Sidebar ---
st.sidebar.header("Navigation")
tabs = st.sidebar.radio("Choose a view:", ["Regulations", "Mappings", "Impact Analysis", "Recommended Actions"])

# --- Tabs ---
if tabs == "Regulations":
    st.header("📜 New Regulatory Updates")
    for doc in results.get("regulatory_updates", []):
        with st.expander(doc.get("title", "Untitled Regulation"), expanded=False):
            st.write(doc.get("content", "No content available"))

elif tabs == "Mappings":
    st.header("🗺️ Regulation → Policies & Controls Mapping")
    for m in results.get("mappings", []):
        with st.expander(m.get("regulation_title", "Untitled Regulation"), expanded=False):
            related = m.get("related_policies_controls", [])
            if not related:
                st.write("_No mappings found._")
            else:
                for r in related:
                    st.markdown(f"- **{r['text']}**")
                    if r.get("metadata"):
                        st.caption(f"Source: {r['metadata'].get('type', 'N/A')}")

elif tabs == "Impact Analysis":
    st.header("🔍 Impact Summaries")
    for impact in results.get("impacts", []):
        with st.expander(impact.get("regulation_title", "Untitled Regulation"), expanded=False):
            st.text_area("Impact Analysis", impact.get("impact_analysis", ""), height=250)

elif tabs == "Recommended Actions":
    st.header("🧭 Compliance Recommendations")
    for action in results.get("actions", []):
        with st.expander(action.get("regulation_title", "Untitled Regulation"), expanded=False):
            st.text_area("Action Plan", action.get("recommended_actions", ""), height=250)

# --- Footer ---
st.markdown("---")
st.caption("Developed as a Proof of Concept – Regulatory Compliance Copilot © 2025")
