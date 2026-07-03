# RAG Security & Risk Assessment Toolkit

A red-teaming and AI-risk-assessment toolkit for a Retrieval-Augmented
Generation (RAG) application. Built to produce two things from one
codebase: a working adversarial test harness (security evidence) and a
risk register with a documented methodology (governance evidence).

## What's in here

- **`app/`** — a small RAG customer-support bot ("NovaBank") with a
  realistic system prompt and guardrails, plus a knowledge base that
  includes deliberately planted vulnerabilities (fake secrets, a hidden
  prompt-injection payload) so there's something real to find.
- **`attacks/`** — a risk taxonomy, a library of attack payloads organized
  by category, a scorer, and a harness that runs the payloads against the
  live app and records results.
- **`results/`** — where the harness writes raw results and the generated
  risk register.
- **`report/`** — methodology write-up and findings summary.
- **`scripts/`** — aggregates raw results into the risk register CSV and
  findings.md.

## Setup

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up an LLM backend** (pick one)
   - **Local (free, recommended to start):** install
     [Ollama](https://ollama.com), then run `ollama pull llama3`
   - **OpenAI:** copy `.env.example` to `.env`, set `RAG_BACKEND=openai`
     and add your `OPENAI_API_KEY`

3. **Build the vector index**
   ```bash
   python -m app.knowledge_base
   ```

4. **Sanity check the app on its own**
   ```bash
   python -m app.rag_app
   ```
   You should get a normal answer about customer service hours.

## Running the audit

```bash
python -m attacks.harness
```

This runs every payload in `attacks/payloads/` against the app, prints a
live pass/fail per test, and writes full results to
`results/raw_results.json`.

Then generate the risk register and findings report:

```bash
python scripts/generate_report.py
```

This produces `results/risk_register.csv` and `report/findings.md`.

## Project structure

```
rag-security-audit/
├── app/
│   ├── rag_app.py            # the RAG target
│   ├── knowledge_base.py     # builds/loads the vector store
│   └── documents/            # knowledge base, incl. planted vulnerabilities
├── attacks/
│   ├── taxonomy.py           # risk category definitions
│   ├── payloads/             # attack prompts by category
│   ├── scorer.py             # scoring logic
│   └── harness.py            # main test runner
├── results/
│   └── risk_register_template.csv
├── report/
│   ├── methodology.md
│   └── findings_template.md
└── scripts/
    └── generate_report.py
```

## What this demonstrates

- **Security:** adversarial prompt testing across a defined taxonomy
  (prompt injection — direct and indirect, data leakage, jailbreak,
  hallucination, availability), automated scoring, and held-out testing
  to check whether guardrails generalize to attack types not specifically
  tuned against during development.
- **Governance:** a documented risk taxonomy mapped to NIST AI RMF
  references, a structured risk register with severity/likelihood, and a
  written methodology — the actual deliverables a risk or GRC function
  would expect from an assessment, not just a bug list.

## Extending this project

Natural next steps, in rough order of effort:

- Add more payloads per category (this is the highest-leverage thing to
  do — the taxonomy and harness are designed to make this a one-line
  addition to a payload list).
- Replace the heuristic scorer with an LLM-as-judge for fuzzier
  categories (jailbreak, hallucination) and compare agreement against the
  current keyword-based approach.
- Add a `severity_score = f(severity, likelihood)` calculation to the risk
  register for a proper heat-map view.
- Build a small Streamlit dashboard over `results/risk_register.csv`.
- Swap in a real (non-toy) open-source RAG app as the target to test
  against something with more realistic complexity.
- Track results over multiple runs/commits to show remediation over time
  — re-run the harness after "fixing" a guardrail and diff the results.
