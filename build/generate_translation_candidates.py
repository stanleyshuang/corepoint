from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MISSING_TRANSLATIONS = PROJECT_ROOT / "tmp" / "missing_translations.txt"
GLOSSARY = PROJECT_ROOT / "prompt" / "translation" / "glossary_psirt.json"
BLACKLIST = PROJECT_ROOT / "prompt" / "translation" / "blacklist_english.json"
OUTPUT = PROJECT_ROOT / "tmp" / "translation_candidates_l2_01.json"
DEFAULT_MODEL = "gpt-5.2"
API_URL = "https://api.openai.com/v1/responses"
DOCUMENT_FORMAT_CONTEXT = (
    "The target MS Word output is a controlled Level 2/QP procedure. "
    "Keep translations concise enough for 12 pt H1/H2/body/list styles and do not add "
    "extra headings, numbering, bullets, or explanatory text that is not present in the source."
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid JSON object: {path}")
    return data


def load_missing(path: Path) -> list[str]:
    items: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def glossary_prompt(glossary: dict) -> str:
    terms = glossary.get("preferred_terms", {})
    acronyms = glossary.get("canonical_acronyms", [])
    lines = ["Preferred terminology:"]
    for zh, en in terms.items():
        lines.append(f"- {zh}: {en}")
    if acronyms:
        lines.append("Canonical acronyms to preserve: " + ", ".join(acronyms))
    return "\n".join(lines)


def blocked_prompt(blacklist: dict) -> str:
    blocked = []
    for entry in blacklist.get("blocked_phrases", []):
        if isinstance(entry, dict) and entry.get("phrase"):
            blocked.append(str(entry["phrase"]))
    return "Do not output any of these blocked phrases: " + ", ".join(blocked)


def request_payload(model: str, sources: list[str], glossary: dict, blacklist: dict) -> dict:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "translations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "source": {"type": "string"},
                        "candidate": {"type": "string"},
                        "status": {"type": "string", "enum": ["draft"]},
                        "review_required": {"type": "boolean"},
                        "risk": {"type": "string", "enum": ["low", "medium", "high"]},
                        "notes": {"type": "string"},
                    },
                    "required": ["source", "candidate", "status", "review_required", "risk", "notes"],
                },
            }
        },
        "required": ["translations"],
    }
    instructions = "\n".join(
        [
            "You are drafting English translations for an IEI PSIRT procedure.",
            "Chinese is the authoritative source. Preserve legal and procedural meaning exactly.",
            DOCUMENT_FORMAT_CONTEXT,
            "Return JSON only according to the schema.",
            "Each output status must be draft and review_required must be true.",
            glossary_prompt(glossary),
            blocked_prompt(blacklist),
        ]
    )
    return {
        "model": model,
        "input": [
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": "Translate each Chinese source string into formal procedure English:\n"
                + json.dumps(sources, ensure_ascii=False, indent=2),
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "translation_candidates",
                "schema": schema,
                "strict": True,
            }
        },
    }


def extract_output_text(response: dict) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]
    parts: list[str] = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                parts.append(content["text"])
    return "\n".join(parts)


def call_openai(payload: dict, api_key: str) -> dict:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API error {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenAI API connection error: {exc}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate draft translation candidates with an external LLM.")
    parser.add_argument("--input", type=Path, default=MISSING_TRANSLATIONS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--model", default=os.environ.get("OPENAI_TRANSLATION_MODEL", DEFAULT_MODEL))
    parser.add_argument("--limit", type=int, help="Translate only the first N missing strings.")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and show planned batches without API calls.")
    args = parser.parse_args()

    for path in (args.input, GLOSSARY, BLACKLIST):
        if not path.exists():
            raise SystemExit(f"Required file not found: {path}")

    sources = load_missing(args.input)
    if args.limit:
        sources = sources[: args.limit]
    glossary = load_json(GLOSSARY)
    blacklist = load_json(BLACKLIST)
    batches = chunked(sources, args.batch_size)

    if args.dry_run:
        print(f"input={args.input}")
        print(f"output={args.output}")
        print(f"model={args.model}")
        print(f"sources={len(sources)}")
        print(f"batches={len(batches)}")
        print("write=false")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required to call the external LLM API.")

    all_candidates = []
    for index, batch in enumerate(batches, start=1):
        payload = request_payload(args.model, batch, glossary, blacklist)
        response = call_openai(payload, api_key)
        text = extract_output_text(response)
        if not text:
            raise SystemExit(f"No output_text returned for batch {index}.")
        parsed = json.loads(text)
        all_candidates.extend(parsed.get("translations", []))
        print(f"batch={index}/{len(batches)} candidates={len(all_candidates)}")
        time.sleep(0.2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "source_file": str(args.input),
        "model": args.model,
        "status": "draft",
        "review_required": True,
        "translations": all_candidates,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
