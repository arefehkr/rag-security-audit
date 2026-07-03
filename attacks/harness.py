"""
Main attack harness.

Runs every payload in attacks/payloads/*.py against the live RAG app,
scores each response, and writes results to results/raw_results.json.

Run from the project root:
    python -m attacks.harness
"""

import json
import os
from datetime import datetime, timezone

from app.rag_app import RAGApp, SYSTEM_PROMPT
from attacks.scorer import score_response
from attacks.payloads.prompt_injection import PROMPT_INJECTION_PAYLOADS
from attacks.payloads.data_leakage import DATA_LEAKAGE_PAYLOADS
from attacks.payloads.jailbreak import JAILBREAK_PAYLOADS
from attacks.payloads.hallucination import HALLUCINATION_PAYLOADS
from attacks.payloads.availability import AVAILABILITY_PAYLOADS

ALL_PAYLOADS = {
    "prompt_injection": PROMPT_INJECTION_PAYLOADS,
    "data_leakage": DATA_LEAKAGE_PAYLOADS,
    "jailbreak": JAILBREAK_PAYLOADS,
    "hallucination": HALLUCINATION_PAYLOADS,
    "availability": AVAILABILITY_PAYLOADS,
}


def run_audit(held_out_categories=None, output_path="results/raw_results.json"):
    """
    held_out_categories: category ids to run as a separate "zero-day" batch
    -- e.g. pass ["jailbreak"] to simulate testing the app against an
    attack class you didn't design the app's guardrails around. This is
    the analogue of confidence-based zero-day evaluation: it tells you
    whether your defenses generalize or whether they're overfit to the
    exact attacks you tested during development.
    """
    held_out_categories = held_out_categories or []
    app = RAGApp()
    results = []

    for category, payloads in ALL_PAYLOADS.items():
        batch = "held_out" if category in held_out_categories else "known"
        for payload in payloads:
            response = app.query(payload["prompt"])
            score = score_response(response["answer"], payload, SYSTEM_PROMPT)

            results.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": category,
                "batch": batch,
                "payload_id": payload["id"],
                "prompt": payload["prompt"],
                "answer": response["answer"],
                "vulnerable": score["vulnerable"],
                "evidence": score["evidence"],
                "notes": payload.get("notes", ""),
            })

            status = "VULNERABLE" if score["vulnerable"] else "ok"
            print(f"[{category}] {payload['id']} -> {status}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    vulnerable_count = sum(1 for r in results if r["vulnerable"])
    print(f"\n{vulnerable_count}/{len(results)} tests found a vulnerability.")
    print(f"Saved full results to {output_path}")
    return results


if __name__ == "__main__":
    # Treat "jailbreak" as the held-out / zero-day-style batch by default --
    # change this list to whichever category you want to test generalization
    # against.
    run_audit(held_out_categories=["jailbreak"])
