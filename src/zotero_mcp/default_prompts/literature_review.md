# Literature Review Prompt

Perform comprehensive academic analysis of paper {item_key}.

## Phase 1: Information Gathering

1. Call `zotero_get_item_metadata("{item_key}")` for bibliographic details and abstract.
2. Call `zotero_get_item_children("{item_key}")` to retrieve annotations and notes.
3. If no annotations found, call `zotero_get_item_fulltext("{item_key}")` to get the full paper text.

## Phase 2: Analysis

Based on the available content, provide analysis for **ALL** of the following fields:

1. **Research Objective** - What is the main research question or goal?
2. **Research Background** - What context, motivation, or prior work is mentioned?
3. **Research Methods** - What methodology, data, or approach is used?
4. **Contribution** - What are the novel contributions or key findings?
5. **Gaps** - What limitations or future work are identified?
6. **Discussion** - What are the implications or broader impact?
7. **Quotes** - Key sentences worth citing (with page numbers if available)
8. **To-Read** - Related papers or references mentioned worth reading

**Analysis Mode:**
- If annotations exist: Prioritize the user's highlights and comments
- If no annotations: Analyze from full text (or abstract if full text unavailable)

**IMPORTANT:** Fill ALL 8 fields above. If information is not available, write "Not explicitly mentioned in the paper" instead of leaving blank.

## Phase 3: Note Creation

After presenting the analysis, ask:
"Would you like me to save this review as a note in Zotero?"

If user agrees, call `zotero_create_review` with **ALL fields filled**:

```
zotero_create_review(
    item_key="{item_key}",
    analysis={
        "objective": "The main research question is...",
        "background": "This paper builds on prior work in...",
        "methods": "The methodology involves...",
        "contribution": "The key contributions are...",
        "gaps": "Limitations include...",
        "discussion": "The implications are...",
        "quotes": "Key findings: '...' (p.X)",
        "to_read": "Related papers: Author (Year), ..."
    }
)
```

**Note:** The system automatically fills metadata (title, authors, year, DOI, abstract) from Zotero. You only need to provide the 8 analysis fields above.
