# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is an IEI PSIRT document automation workspace. Its primary output is a bilingual (Chinese/English) MS Word procedure document (`doc/QP-30-01 事件處理程序 V1.0.docx`) generated from a Markdown source (`doc/L2-01_vulnerability-handling-and-disclosure-process.md`).

## Environment Setup

Python dependencies are isolated in `.venv/`. Never use the system Python.

```bash
python3 -m venv .venv
.venv/bin/pip install python-docx
```

## Build Commands

**Dry-run (validate paths, styles, translation memory, and Mermaid hash without writing):**
```bash
.venv/bin/python build/build_qp_docx.py \
  --source doc/L2-01_vulnerability-handling-and-disclosure-process.md \
  --template template/樣本.docx \
  --document-control-template template/文件管制程序2.7.doc \
  --flow-image template/vul_handle_n_disclose_flow.png \
  --output "doc/QP-30-01 事件處理程序 V1.0.docx" \
  --dry-run
```

**Generate DOCX** (same flags without `--dry-run`). If the output file already exists, a `_YYYYMMDD` suffix is appended automatically; never overwrites.

All default paths shown above are overridable — see `main()` in `build/build_qp_docx.py` for the full flag list (`--project-root`, `--translation-dir`, `--glossary`, `--blacklist`, `--translation-memory`, `--missing-translation-report`, `--blocked-english-report`, `--source-start-pattern`, `--known-mermaid-sha256`, `--date-suffix`). Notably `--known-mermaid-sha256` and `--date-suffix` let you override the Mermaid fail-fast hash and the output-naming date suffix without editing the script.

**Translation pipeline** (run only when `tmp/missing_translations.txt` is non-empty after a failed build):
```bash
# 1. Generate LLM draft candidates (requires OPENAI_API_KEY)
OPENAI_API_KEY=... .venv/bin/python build/generate_translation_candidates.py --dry-run
OPENAI_API_KEY=... .venv/bin/python build/generate_translation_candidates.py --limit <N>

# 2. Local quality review
.venv/bin/python build/review_translation_candidates.py
# Output: tmp/translation_review_l2_01.json
```

The `_l2_01` filenames above are the script defaults (`generate_translation_candidates.py` writes `tmp/translation_candidates_l2_01.json`; `review_translation_candidates.py` reads it and writes `tmp/translation_review_l2_01.json`). Any `*_test.json` files under `tmp/` are throwaway working files, not pipeline outputs.

After human review, manually add approved entries to `prompt/translation/translation_memory_l2_01.json`.

## Architecture

```
doc/          # Markdown source + DOCX outputs (DOCX is git-ignored except template/)
build/        # Python build scripts
template/     # Word template, document control reference, flow diagram PNG
prompt/         # dated top-level *.md files are working prompts (e.g. 260528.L2-01...md)
  translation/  # glossary_psirt.json, blacklist_english.json, translation_memory_l2_01.json
  workflow/     # markdown_convert_msword.md — the authoritative DOCX conversion spec
  _general/     # Company/law reference context
  _analysis/, gap_analysis/  # Workflow + standards gap-analysis notes
  iec/, cra/    # Regulatory reference prompts
  iei/          # Company reference info
  qnap_29147_30111/, security_incident_response_procedures/  # PSIRT process references
persona/      # Role definitions used when prompting Claude for document tasks
plan/         # Architectural decisions and document restructuring plans
tmp/          # Working files (git-ignored): missing_translations.txt, candidate/review JSON
```

## Key Rules and Constraints

**DOCX generation is strictly controlled:**
- All output DOCX must be produced by `build/build_qp_docx.py`. No manual saves, ad-hoc scripts, or copy-paste from existing DOCX.
- `prompt/workflow/markdown_convert_msword.md` is the single authoritative spec for Word conversion rules. Do not redefine styles, font sizes, or output naming anywhere else.

**Translation memory is the only trusted English source:**
- English text in the DOCX comes exclusively from `prompt/translation/translation_memory_l2_01.json`, hardcoded strings in `build_qp_docx.py`, and `prompt/translation/glossary_psirt.json`.
- LLM-generated candidates (`tmp/translation_candidates_l2_01.json`) are always `draft`; they require human review before entering the translation memory.
- `legal_review_required` items must be approved by legal/compliance before entering the memory.

**Fail-fast gates** (build aborts if any of these fail):
- Source content start pattern not found in Markdown
- Mermaid block SHA-256 does not match `KNOWN_MERMAID_SHA256` in `build_qp_docx.py`
- Missing English translation for any Chinese paragraph
- English output matches a phrase in `blacklist_english.json`
- Required Word styles missing or effective font size ≠ 12pt in `template/樣本.docx`

**Style rules enforced by `build_qp_docx.py`:**
- Required styles: `Normal`, `H1`–`H5`, `H2_EN`–`H5_EN`, `Body`, `Body EN`, `List Paragraph` — all must be 12pt in `template/樣本.docx`.
- Style aliases (e.g. `BodyEN` → `Body EN`) are resolved before writing; fallback to `Normal` is a bug.
- English paragraphs inherit paragraph formatting (indent, line spacing, alignment, etc.) from their paired Chinese paragraph.

**Mermaid → PNG replacement:**
- The single Mermaid block in the source Markdown is replaced by `template/vul_handle_n_disclose_flow.png` in the DOCX.
- If the Mermaid content changes, update the PNG first, then update `KNOWN_MERMAID_SHA256` in `build_qp_docx.py`.

**Source content boundary:**
- DOCX body starts at `## 1. 目的 Purpose` (or `## 目的 Purpose`). Everything before it (document control metadata) is excluded.
- Heading numbers are stripped in DOCX output: `## 1. 目的 Purpose` → `目的 Purpose`.

**Output naming:**
- Existing output file → `_YYYYMMDD` suffix → `_YYYYMMDD_v2`, `_v3`, … Never overwrites.

## AGENTS.md Role

`AGENTS.md` defines the standing persona for this repo: IEI PSIRT Senior PM, responding in Traditional Chinese, familiar with ISO/IEC 29147, ISO/IEC 30111, CRA, and SBOM/supply-chain security. All responses should follow the structured format (confirmed facts / reasonable assumptions / risk judgments / recommended actions) defined there. It also mandates:
- A **"可優化之處" (areas for improvement)** note after every task — what could be omitted, what needs more precise specification, quality/accuracy/executability suggestions.
- An **8-step implementation-approval gate**: confirm requirements → ask clarifying questions → list tentative assumptions → propose a design → explain trade-offs/risks → adjust per feedback → implement only after explicit approval. Low-risk single-turn tasks may proceed after briefly stating assumptions.
