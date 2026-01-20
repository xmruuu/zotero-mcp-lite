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

## Phase 2: Thorough Analysis

Extract comprehensive information for each field.

### Output Rules

1. **Be thorough** - Include sufficient detail for future reference
2. **No meta-commentary** - Skip "The authors mention...", "In this paper...", etc.
3. **Direct statements only** - Jump straight to the point
4. **Quote when valuable** - Capture key phrases that define the work
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
objective: [Intro] Develop a few-shot object detection framework for construction safety compliance monitoring that can identify safety violations with minimal training data, addressing the challenge of limited labeled datasets in construction site imagery.

methods: [Methods] Created custom dataset of 5,000 construction site images across 12 object classes (helmets, vests, harnesses, etc.). Implemented YOLO-based detector with transfer learning from COCO pre-trained weights. Used 5-shot learning protocol with episodic training. Evaluation on held-out test set of 1,000 images from 3 different construction sites.

contribution: [Results] Achieved 88.2% precision and 79.5% recall for object detection tasks; 94.8% accuracy for safety attribute recognition. Outperformed baseline models by 15% on few-shot scenarios. Demonstrated generalization across different construction site types and lighting conditions.

gaps: [Limitations] Focus limited to fall-related hazards only; no real-time deployment tested on live construction sites; dataset biased toward daytime conditions; does not address occlusion scenarios common in crowded work areas.

to_read: Wang et al. (2023) - provides larger-scale safety image dataset (50K images) for comparison; Chen (2022) - addresses real-time detection gap with edge deployment; Kim (2024) - covers multi-hazard detection beyond fall protection.
```

## Phase 3: Note Creation

After presenting the analysis, ask:
"Would you like me to save this review as a note in Zotero?"

If user agrees, call `zotero_create_review`:

```
zotero_create_review(
    item_key="{item_key}",
    analysis={
        "objective": "[Intro] Full research goal with context and motivation.",
        "background": "[Related Work] Key prior work with specific contributions: Author A (Year) established X; Author B (Year) advanced Y but left gap Z.",
        "methods": "[Methods] Complete methodology description including data sources, sample sizes, algorithms/frameworks used, and validation approach.",
        "contribution": "[Results] Detailed findings with metrics, comparisons to baselines, and significance of improvements.",
        "gaps": "[Limitations] What the authors acknowledge they didn't address, methodological constraints, and scope boundaries.",
        "discussion": "[Conclusion] Future research directions suggested by authors and implications for the field.",
        "quotes": "Multiple key quotes that capture the essence of the work, each with [Section] reference.",
        "to_read": "Relevant references with specific reasons: Author (Year) - why this paper fills a gap or provides complementary insight."
    }
)
```

**Reminder:** Metadata (title, authors, year, DOI, abstract) is auto-filled. Focus on thorough, verifiable insights.
