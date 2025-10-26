# 🧩 Regulatory Compliance Copilot — AI PoC

**Regulatory Compliance Copilot** is an **Agentic AI Proof-of-Concept** designed for the **UK banking domain**.  
It automates **regulatory monitoring**, **policy impact assessment**, and **compliance action planning** using large language models (LLMs).

---

## 🚀 Overview

Banks and financial institutions spend thousands of hours manually reviewing **FCA** and **PRA** updates to assess their impact on internal policies and controls.  
This PoC demonstrates how an **AI Copilot** can assist compliance teams by:

1. **Ingesting** new regulations from trusted sources (e.g., FCA, PRA, BoE)  
2. **Summarizing** the updates for quick review  
3. **Mapping** them to relevant internal policies and controls  
4. **Analyzing** business impact and identifying compliance gaps  
5. **Recommending** prioritized actions for remediation or policy updates  

> 🧠 The Copilot acts as a digital assistant for compliance teams — enabling faster, explainable, and auditable regulatory alignment.

---

## 🏗️ Architecture

```text
 ┌────────────────────────────┐
 │ Regulatory Sources (FCA,   │
 │ PRA, BoE, Mock Data)       │
 └────────────┬───────────────┘
              │
              ▼
      [Regulation Ingestion Agent]
              │
              ▼
      [Policy Mapping Agent]
              │
              ▼
      [Impact Analysis Agent]
              │
              ▼
      [Action Recommendation Agent]
              │
              ▼
        [Streamlit Dashboard]

```
## ⚙️ Tech Stack

| Component              | Technology                        |
|------------------------|-----------------------------------|
| Language / Framework   | Python 3.10+, Streamlit           |
| AI / LLM               | OpenAI (via LangChain ChatOpenAI) |
| Vector Store           | ChromaDB                          |
| Data Parsing           | BeautifulSoup (for web scraping)  |
| Logging                | Loguru                            |
| Environment Management | python-dotenv                         |
| UI                      | Streamlit dashboard                         |
| Version Control           | Git / GitHub                          |

## 🧰 Quick Start
1️⃣ Setup environment

```
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2️⃣ Configure environment variables

Create a .env file in the project root:
```
OPENAI_API_KEY=sk-your-api-key
FORCE_REFRESH=false
```

3️⃣ Run the main workflow
```
python src/main.py
```
* Loads mock or live FCA/PRA updates
* Summarizes and analyzes regulatory impacts
* Saves results to src/data/output/compliance_analysis.json

4️⃣ Launch the UI Dashboard
```
streamlit run src/ui/streamlit_dashboard.py
```
Displays the summarized regulations, impact analysis, and recommended compliance actions.

## 📊 Example Output

**Example Regulation:** FCA Conduct Risk Update 2024
**Impact Summary:** Increased monitoring and reporting standards for retail banking.
**Identified Gaps:** Outdated internal policy on customer communications.
**Recommended Actions:**
* Update Conduct Risk Policy (Priority: High, Timeline: Q1 2025)
* Retrain frontline staff on FCA fairness principles

## 🧠 Key Highlights

* ✅ Modular Agentic AI design (Ingestion → Mapping → Impact → Action)
* ✅ Supports mock and live modes (switch via .env)
* ✅ Explainable LLM outputs for traceability
* ✅ Extendable to other domains — ESG, Risk, AML monitoring
* ✅ Built with production-style structure ready for scaling

## 📦 Project Structure
```
src/
 ├── agents/
 │    ├── ingestion_agent.py
 │    ├── mapping_agent.py
 │    ├── impact_agent.py
 │    └── action_agent.py
 ├── core/
 │    ├── llm_client.py
 │    ├── retriever.py
 │    └── workflow.py
 ├── ui/
 │    └── streamlit_dashboard.py
 ├── utils/
 │    └── logger.py
 ├── data/
 │    ├── regulatory_updates/
 │    └── output/
 └── main.py
```

## 🔒 Security Notes

* .env (containing API keys) is excluded via .gitignore.
* Only mock/sample data is stored under /data/regulatory_updates/.
* Vector store and cache outputs are not committed to the repository.

## 📈 Future Enhancements

* “Refresh Data” button in Streamlit (to trigger a new run)
* Display “Last Updated” timestamp in dashboard
* Integrate document similarity clustering for impact grouping
* Add explainability layer using OpenAI function calling