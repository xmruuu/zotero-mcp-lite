# Literature Review Prompt

User request: {paper}

## Step 1: Find the Paper

First, identify which paper to review:

- If user mentions a title/topic → Use `zotero_search_items(query)` to find it
- If user says "recent paper" or "paper I just added" → Use `zotero_get_recent(limit=1)`
- If user provides an item key directly → Use that key
- If unclear → Ask the user which paper to review

## Step 2: Gather Information

1. Call `zotero_get_item_metadata(item_key)`
2. Call `zotero_get_item_children(item_key)` for annotations
3. If annotations are sparse, call `zotero_get_item_fulltext(item_key)`

## Step 3: Analysis

Analyze the paper under these sections. Use tables, bullet points, or prose as appropriate:

- **Research Objective** - What problem does this paper solve?
- **Research Background** - Key prior work and research gap
- **Research Methods** - How did they do it?
- **Contribution** - What did they find/achieve?
- **Research Gaps** - Limitations acknowledged by authors
- **Discussion** - Future directions and implications
- **Key Quotes** - Important statements from the paper
- **To-Read** - Related papers worth reading and why

### Rules

- Extract only explicit content from the paper
- If information not found, write "Not discussed"
- Never fabricate data or citations

## Step 4: Save to Zotero

Ask: "Save this review to Zotero?"

If yes, call `zotero_create_review` with the analysis content.
