---
name: omim-browser-research
description: Operate the user's browser with Codex to collect OMIM Clinical Synopsis search results, extract ocular and systemic features and molecular basis, translate disease names, resume interrupted work, and export an Excel workbook. Use for OMIM browser-based research collection, not browser extension development.
---

# OMIM browser research

This skill orchestrates existing Codex browser and spreadsheet tools. It does not install a browser extension, create remote access, or run unattended after a chat stops. Creating this skill is not collecting the dataset. Read `references/records.md` before extraction.

## Browser workflow

1. Use the available computer-use skill and `mcp__cua_repl` browser documentation. Select the user's specified tab or search URL. If none is specified, inspect available tabs before asking. Use browser UI tools for all navigation, page reading and clicks. Do not substitute shell HTTP, injected scrapers, undocumented browser evaluation, cookies or hidden endpoints. Request login/challenge handling from the user when necessary; do not bypass access controls. Do not change the search silently.
2. Record the exact search URL, visible query, displayed count and collection date in a task-specific `run.json`. Expected count is read from the page, not hardcoded to 3,506. Use `outputs/omim-runs/<date-and-short-run-id>/` for each distinct search snapshot. Never combine different searches silently.
3. First validate extraction on three varied real results: one with Eyes and molecular basis, one without Eyes, and one with multiple genes if present. Confirm the disease name and six-digit phenotype MIM number against that result's heading. Do not mistake linked gene MIM numbers for the phenotype identifier.
4. On each search page, save its visible disease IDs and titles to `pages.jsonl`. Expand each observed `View full synopsis below` control and observe the updated state. Use the smallest supported read of the expanded synopsis. Obtain fresh state before choosing the next control. If expansion fails, use the observed `View full synopsis on new page` link. Never guess selectors or repeat stale element indices. A row may be complete only after the full expanded synopsis has been read, including the lower sections.
5. Capture raw text and source URL before summarizing. Separate HEAD & NECK / Eyes from other subheadings (Face, Ears, etc.). Preserve qualifiers, negative findings, onset, laterality and frequency. Capture all major systemic features by system; do not arbitrarily truncate to the first three bullets. Retain inheritance and miscellaneous information in raw evidence even if not included in the six principal columns.
6. Extract gene symbols from MOLECULAR BASIS with supporting text. Preserve mitochondrial symbols and multiple genes. Do not interpret every linked six-digit identifier as a gene symbol. Distinguish unknown gene, chromosome abnormality, absent molecular-basis section and failed reading. When uncertain, retain the original sentence and flag it; do not infer a cause from a disease name.
7. Translate the English disease name into Chinese using an available established name; otherwise use a faithful translation marked 暂译. Keep subtype numbers and gene symbols. The six principal columns use English original feature text by default; provide an additional Chinese summary only if requested. If the user requests translated symptoms, retain original text alongside translations. Codex performs translation; the storage script does not translate or diagnose. Mark unresolved translations pending, not complete.
8. Save each small batch using `scripts/records.py ingest`; it validates evidence and stores records transactionally in SQLite keyed by phenotype MIM. Use `status` to see pending IDs. Record page URL and the next unread ID in `run.json` after every page. Resume from these files, verifying the current browser page and already saved IDs. Keep explicit error records for inaccessible results. Pause collection on a challenge/rate limit and preserve progress. Do not spin on repeated failures.
9. Navigate with the observed Next link and verify page/index change. Compare the union of page IDs, saved unique IDs and displayed result count. Detect duplicate/repeated pages. A missing Eyes section is not a missing record: retain it as 无眼部条目 for review. Do not discard records to make the count fit.

## Excel and completion

Use the available spreadsheets skill and bundled dependencies. `records.py export` produces JSON for `scripts/export.mjs`, which uses `@oai/artifact-tool`. Place/run a copy of the exporter beside a node_modules junction to bundled dependencies, per spreadsheet skill setup. Run its authoring marker before creating the workbook. Inspect the resulting workbook and render a representative range with the spreadsheet tools before delivery.

Principal columns: 英文名、OMIM编号、中文译名、眼部相关症状、其他器官或系统的主要症状、致病基因. Add provenance/status columns and a second sheet with original synopsis and molecular basis. Never silently truncate a cell beyond Excel's limit; split evidence into numbered chunks.

Before reporting complete: all unique listed IDs accounted for, every completed row has raw evidence and source, translation status checked, failures listed separately, first/middle/last pages reconciled. A partial workbook must say 部分完成 and show collected / expected / failed counts. A search result count is a count of OMIM entries, not automatically distinct clinical disease families. Report count basis and snapshot date.

Do not upload collected data to GitHub or a public site as part of this collection task. An earlier Orphanet workflow does not determine OMIM reuse terms. Retain any source notices and use the access actually granted to the user.
