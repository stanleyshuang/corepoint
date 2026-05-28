from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = PROJECT_ROOT / "tmp" / "translation_candidates_l2_01.json"
GLOSSARY = PROJECT_ROOT / "prompt" / "translation" / "glossary_psirt.json"
BLACKLIST = PROJECT_ROOT / "prompt" / "translation" / "blacklist_english.json"
OUTPUT = PROJECT_ROOT / "tmp" / "translation_review_l2_01.json"

HIGH_RISK_PATTERNS = (
    "CRA",
    "Article 14",
    "24",
    "72",
    "10 年",
    "5 年",
    "3 年",
    "1 年",
    "主管機關",
    "通報",
    "保存",
    "揭露",
    "責任",
    "法遵",
    "二階文件",
    "文件編寫",
    "文件管制",
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid JSON object: {path}")
    return data


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def blocked_hits(text: str, blacklist: dict) -> list[str]:
    lowered = text.lower()
    hits = []
    for entry in blacklist.get("blocked_phrases", []):
        if isinstance(entry, dict) and entry.get("phrase") and entry["phrase"].lower() in lowered:
            hits.append(entry["phrase"])
    return hits


def terminology_warnings(source: str, candidate: str, glossary: dict) -> list[str]:
    warnings = []
    terms = glossary.get("preferred_terms", {})
    for zh, en in terms.items():
        if zh in source and en.lower() not in candidate.lower():
            warnings.append(f"expected term: {zh} -> {en}")
    for acronym in glossary.get("canonical_acronyms", []):
        if acronym in source and acronym not in candidate:
            warnings.append(f"missing acronym: {acronym}")
    return warnings


def numeric_tokens(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def review_item(item: dict, glossary: dict, blacklist: dict) -> dict:
    source = str(item.get("source", "")).strip()
    candidate = str(item.get("candidate", "")).strip()
    issues = []
    status = "approved"

    hits = blocked_hits(candidate, blacklist)
    if hits:
        status = "blocked"
        issues.extend(f"blocked phrase: {hit}" for hit in hits)

    if not candidate:
        status = "blocked"
        issues.append("empty candidate")

    if has_cjk(candidate):
        status = "needs_revision" if status == "approved" else status
        issues.append("candidate contains CJK characters")

    missing_numbers = numeric_tokens(source) - numeric_tokens(candidate)
    if missing_numbers:
        status = "needs_revision" if status == "approved" else status
        issues.append("numeric tokens missing: " + ", ".join(sorted(missing_numbers)))

    term_warnings = terminology_warnings(source, candidate, glossary)
    if term_warnings:
        status = "needs_revision" if status == "approved" else status
        issues.extend(term_warnings)

    if any(pattern in source for pattern in HIGH_RISK_PATTERNS) and status == "approved":
        status = "legal_review_required"
        issues.append("high-risk legal/process wording requires reviewer approval")

    reviewed = dict(item)
    reviewed["review_status"] = status
    reviewed["review_issues"] = issues
    return reviewed


def main() -> None:
    parser = argparse.ArgumentParser(description="Review draft translation candidates with local quality gates.")
    parser.add_argument("--input", type=Path, default=CANDIDATES)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    for path in (args.input, GLOSSARY, BLACKLIST):
        if not path.exists():
            raise SystemExit(f"Required file not found: {path}")

    candidates = load_json(args.input)
    glossary = load_json(GLOSSARY)
    blacklist = load_json(BLACKLIST)

    reviewed = [
        review_item(item, glossary, blacklist)
        for item in candidates.get("translations", [])
        if isinstance(item, dict)
    ]
    summary = {}
    for item in reviewed:
        summary[item["review_status"]] = summary.get(item["review_status"], 0) + 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "source_file": str(args.input),
        "summary": summary,
        "translations": reviewed,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
