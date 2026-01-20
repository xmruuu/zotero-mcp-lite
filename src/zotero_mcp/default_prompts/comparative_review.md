# Comparative Review Prompt

Synthesize a comparative review for papers: {keys_list}

## Phase 1: Information Gathering

For EACH paper:
1. Call `zotero_get_item_metadata(key)` for bibliographic info
2. Call `zotero_get_item_children(key)` for annotations

## Phase 2: Comparative Analysis

Create a synthesis covering:

1. **Papers Overview** - Title, authors, year for each
2. **Themes** - Common topics across papers
3. **Methods** - How approaches differ
4. **Consensus** - Where authors agree
5. **Conflicts** - Disagreements or tensions
6. **Evolution** - How the field has evolved
7. **Gaps** - Shared limitations
8. **Synthesis** - Overall narrative

## Phase 3: Note Creation

After presenting analysis, ask:
"Would you like me to save this comparative review as a note?"

If user agrees, call `zotero_create_review` with the analysis:

```
zotero_create_review(
    item_key="{first_key}",
    analysis={
        "papers": "Paper 1: ...; Paper 2: ...",
        "themes": "Common themes include...",
        "methods": "Methodological differences...",
        "consensus": "Authors agree on...",
        "conflicts": "Key debates include...",
        "evolution": "The field has evolved...",
        "gaps": "Shared limitations...",
        "synthesis": "Overall, these papers..."
    },
    template_name="comparative_review"
)
```

The system will automatically fill in metadata from Zotero.
