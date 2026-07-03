"""
Aggregates results/raw_results.json into:
  - results/risk_register.csv  (governance-style artifact)
  - report/findings.md         (human-readable summary)

Run from the project root after running the harness:
    python scripts/generate_report.py
"""

import csv
import json
import os
from collections import defaultdict

from attacks.taxonomy import RISK_TAXONOMY

SEVERITY_MAP = {t["id"]: t["base_severity"] for t in RISK_TAXONOMY}
NIST_REF_MAP = {t["id"]: t["nist_ai_rmf_ref"] for t in RISK_TAXONOMY}


def load_results(path="results/raw_results.json"):
    with open(path) as f:
        return json.load(f)


def build_risk_register(results, output_csv="results/risk_register.csv"):
    grouped = defaultdict(list)
    for r in results:
        grouped[r["category"]].append(r)

    rows = []
    for category, items in grouped.items():
        total = len(items)
        vulnerable = [i for i in items if i["vulnerable"]]
        rate = len(vulnerable) / total if total else 0
        likelihood = "High" if rate > 0.5 else ("Medium" if vulnerable else "Low")

        rows.append({
            "risk_category": category,
            "severity": SEVERITY_MAP.get(category, "Medium"),
            "nist_ai_rmf_ref": NIST_REF_MAP.get(category, ""),
            "likelihood": likelihood,
            "tests_run": total,
            "vulnerabilities_found": len(vulnerable),
            "example_finding": vulnerable[0]["payload_id"] if vulnerable else "",
            "status": "Open" if vulnerable else "No issues found",
            "recommended_remediation": "",  # fill in manually per finding
        })

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Risk register written to {output_csv}")
    return rows


def build_findings_md(results, output_path="report/findings.md"):
    grouped = defaultdict(list)
    for r in results:
        grouped[r["category"]].append(r)

    lines = ["# Findings\n", "_Auto-generated from results/raw_results.json. Edit freely._\n"]

    for category, items in grouped.items():
        vulnerable = [i for i in items if i["vulnerable"]]
        lines.append(f"\n## {category.replace('_', ' ').title()}")
        lines.append(f"- Tests run: {len(items)}")
        lines.append(f"- Vulnerabilities found: {len(vulnerable)}")
        for v in vulnerable:
            lines.append(f"\n**{v['payload_id']}** ({v['batch']} batch)")
            lines.append(f"- Prompt: `{v['prompt']}`")
            lines.append(f"- Evidence: {v['evidence']}")
            lines.append(f"- Notes: {v['notes']}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Findings summary written to {output_path}")


if __name__ == "__main__":
    results = load_results()
    build_risk_register(results)
    build_findings_md(results)
