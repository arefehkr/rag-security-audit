# Methodology

## Scope
This assessment targets a single RAG (Retrieval-Augmented Generation)
customer-support application ("NovaBank support bot") built for this
project. The system consists of:
- A document knowledge base (`app/documents/`)
- A vector store (Chroma) for retrieval
- An LLM (local via Ollama, or OpenAI) that generates answers grounded in
  retrieved context

## Risk Taxonomy
Risks are organized into five categories, defined in `attacks/taxonomy.py`
and loosely mapped to NIST AI RMF functions:

| Category | Description | Severity |
|---|---|---|
| Prompt Injection | Direct or indirect attempts to override system instructions | High |
| Data / Metadata Leakage | Disclosure of sensitive knowledge-base content | Critical |
| Jailbreak / Policy Bypass | Guardrail bypass via role-play or framing | Medium |
| Hallucination | Confident fabrication of unsupported facts | Medium |
| Availability | Resource exhaustion via oversized/repetitive requests | Low |

## Test Design
Each category has a small library of attack payloads
(`attacks/payloads/*.py`). Two scoring approaches are used:
- **Marker-based**: checks for an exact signature of successful attack
  (e.g., a planted secret string appearing in the output). Used where
  success has an unambiguous signature -- prompt injection, data leakage.
- **Heuristic**: keyword/length-based checks. Used where success is fuzzier
  -- jailbreak, hallucination, availability. Documented as an approximation;
  see Limitations.

## Zero-Day / Robustness Testing
One category is held out and run as a separate "held_out" batch
(`attacks/harness.py`, `held_out_categories` argument) to test whether the
app's guardrails generalize to attack types not specifically tuned against
during development -- the same logic as testing a detection model against
unseen attack behavior.

## Limitations
- Heuristic scoring will produce some false positives/negatives; every
  "vulnerable" flag should be manually reviewed before being treated as a
  confirmed finding.
- The payload library is illustrative, not exhaustive. A production
  assessment would draw from a much larger, continuously updated payload
  set (e.g., OWASP Top 10 for LLM Applications).
- All planted "sensitive" data is synthetic.

## Tools
Python, LangChain, Chroma, sentence-transformers, Ollama/OpenAI.
