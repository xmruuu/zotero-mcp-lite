# Literature Review Prompt

Perform comprehensive academic analysis of paper {item_key}.

## Phase 1: Information Gathering (MANDATORY)

Execute these steps **in order**:

1. Call `zotero_get_item_metadata("{item_key}")` for bibliographic details.
2. Call `zotero_get_item_children("{item_key}")` to check for annotations.
3. **ALWAYS** call `zotero_get_item_fulltext("{item_key}")` to get the full paper text.

**You MUST read the full text to provide substantive analysis.** Do not rely solely on the abstract.

## Phase 2: Deep Analysis

After reading the full text, provide **detailed and substantive** analysis for each field:

### Required Analysis Fields (ALL must be filled with real content)

| Field | What to Extract | Minimum Requirement |
|-------|-----------------|---------------------|
| **objective** | Research question, hypothesis, or goal | 2-3 sentences explaining what the paper aims to achieve |
| **background** | Literature context, motivation, problem statement | 2-3 sentences on prior work and why this research matters |
| **methods** | Data sources, methodology, experimental design | 2-3 sentences describing how the research was conducted |
| **contribution** | Novel findings, key results, performance metrics | 2-3 sentences on what's new and quantitative results if available |
| **gaps** | Limitations stated by authors, potential weaknesses | 2-3 sentences on what the paper doesn't address |
| **discussion** | Implications, applications, future directions | 2-3 sentences on broader impact and what comes next |
| **quotes** | Important sentences worth citing | 2-3 direct quotes with context |
| **to_read** | Referenced papers worth following up | 2-3 specific paper citations mentioned in the text |

**Analysis Quality Guidelines:**
- Extract **specific details** from the full text, not generic summaries
- Include **numbers, metrics, and concrete findings** where available
- For quotes, cite **actual sentences** from the paper
- For to_read, list **actual paper titles or author names** mentioned

## Phase 3: Note Creation

After presenting the analysis, ask:
"Would you like me to save this review as a note in Zotero?"

If user agrees, call `zotero_create_review` with substantive content in ALL fields:

```
zotero_create_review(
    item_key="{item_key}",
    analysis={
        "objective": "[Specific research goal extracted from introduction]",
        "background": "[Prior work and context from literature review section]",
        "methods": "[Detailed methodology from methods section]",
        "contribution": "[Key findings with metrics from results section]",
        "gaps": "[Limitations from discussion/conclusion section]",
        "discussion": "[Implications and future work from conclusion]",
        "quotes": "[Direct quotes: 'exact text' - context]",
        "to_read": "[Author1 (Year) - title; Author2 (Year) - title]"
    }
)
```

**Reminder:** Metadata (title, authors, year, DOI, abstract) is auto-filled from Zotero. Focus your analysis on insights from the FULL TEXT.
