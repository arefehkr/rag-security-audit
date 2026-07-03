"""
Risk taxonomy for the RAG application under test.

Each category maps loosely to a NIST AI RMF function/subcategory so the
final risk register reads as a governance artifact, not just a bug list.
This mapping is illustrative -- for a real assessment, review the actual
NIST AI RMF (or your organization's framework of choice) and map properly.
"""

RISK_TAXONOMY = [
    {
        "id": "prompt_injection",
        "name": "Prompt Injection",
        "description": (
            "Attacker-controlled input -- entered directly or embedded in "
            "retrieved documents -- overrides the system's intended "
            "instructions."
        ),
        "nist_ai_rmf_ref": "MANAGE 1.1 / GOVERN 1.5",
        "base_severity": "High",
    },
    {
        "id": "data_leakage",
        "name": "Data / Metadata Leakage",
        "description": (
            "The system discloses sensitive information present in its "
            "knowledge base or context that should not be surfaced to "
            "the user."
        ),
        "nist_ai_rmf_ref": "MAP 2.3 / MANAGE 2.2",
        "base_severity": "Critical",
    },
    {
        "id": "jailbreak",
        "name": "Jailbreak / Policy Bypass",
        "description": (
            "The model can be manipulated into ignoring its behavioral "
            "guardrails through role-play, fictional framing, or "
            "instruction-override tricks."
        ),
        "nist_ai_rmf_ref": "GOVERN 1.5 / MANAGE 1.3",
        "base_severity": "Medium",
    },
    {
        "id": "hallucination",
        "name": "Hallucination",
        "description": (
            "The model fabricates confident-sounding answers about topics "
            "not covered by its knowledge base instead of acknowledging "
            "uncertainty."
        ),
        "nist_ai_rmf_ref": "MAP 2.2 / MEASURE 2.5",
        "base_severity": "Medium",
    },
    {
        "id": "availability",
        "name": "Availability / Resource Exhaustion",
        "description": (
            "Requests designed to consume excessive compute or output "
            "length, degrading service for other users."
        ),
        "nist_ai_rmf_ref": "MANAGE 4.1",
        "base_severity": "Low",
    },
]

SEVERITY_ORDER = ["Low", "Medium", "High", "Critical"]
