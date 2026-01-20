# Literature Review Prompt

Perform comprehensive academic analysis of paper {item_key}.

## Phase 1: Smart Information Gathering

Execute these steps **in order**:

1. Call `zotero_get_item_metadata("{item_key}")` for bibliographic details.
2. Call `zotero_get_item_children("{item_key}")` to retrieve annotations and notes.

### Conditional Full Text Retrieval

**Evaluate the annotations:**
- If annotations **cover all 8 analysis fields** → Use annotations as primary source
- If annotations are **sparse or missing key fields** → Call `zotero_get_item_fulltext("{item_key}")` to supplement

**Priority:** User annotations > Full text > Abstract only

This saves tokens and respects the user's reading insights.

## Phase 2: Concise Analysis

Extract information for each field with **strict brevity**.

### Output Rules

1. **Max 50 words per field** - Be concise, no filler
2. **No meta-commentary** - Skip "The authors mention...", "In this paper...", etc.
3. **Direct statements only** - Jump straight to the point
4. **Quote sparingly** - Only when exact wording matters
5. **Cite section** - Use `[Intro]`, `[Methods]`, `[Results]`, etc.

### Anti-Hallucination Rules

1. **Extract only explicit content** - No invention
2. **If not found:** Write "Not discussed"
3. **If inferred:** Mark with `[Inferred]`
4. **Never fabricate** numbers, names, or citations

### Required Analysis Fields

| Field | What to Extract | Notes |
|-------|-----------------|-------|
| **objective** | Research question/goal | From Introduction |
| **background** | Key prior work cited | 2-3 foundational references max |
| **methods** | Methodology + sample size + data source | Be specific: "N=500 survey responses from X" |
| **contribution** | Key findings with metrics | Include exact numbers when available |
| **gaps** | Limitations stated by authors | What they acknowledge they didn't do |
| **discussion** | Future work directions | What authors suggest as next steps |
| **quotes** | 2-3 key sentences | With `[Section]` reference |
| **to_read** | Gap-filling references | Why each is worth reading (e.g., "provides X data this paper lacks") |

### Example Output Format

```
objective: [Intro] Develop few-shot object detection for construction safety compliance.

methods: [Methods] Custom dataset of 5,000 images; YOLO-based detector with transfer learning; N=12 object classes.

contribution: [Results] 88.2% precision, 79.5% recall for object detection; 94.8% for attribute recognition.

gaps: [Limitations] Only fall-related hazards; no real-time deployment tested.

to_read: Wang et al. (2023) - provides larger safety image dataset; Chen (2022) - addresses real-time detection gap.
```

## Phase 3: Note Creation

After presenting the analysis, ask:
"Would you like me to save this review as a note in Zotero?"

If user agrees, call `zotero_create_review`:

```
zotero_create_review(
    item_key="{item_key}",
    analysis={
        "objective": "[Intro] Concise goal statement.",
        "background": "[Related Work] Key refs: A (Year), B (Year).",
        "methods": "[Methods] Methodology, N=X, data from Y.",
        "contribution": "[Results] Key finding with X% metric.",
        "gaps": "[Limitations] What wasn't addressed.",
        "discussion": "[Conclusion] Suggested future work.",
        "quotes": "'Key quote 1' [Section]; 'Key quote 2' [Section]",
        "to_read": "Author (Year) - reason to read; Author (Year) - reason to read"
    }
)
```

**Reminder:** Metadata (title, authors, year, DOI, abstract) is auto-filled. Focus on concise, verifiable insights.
