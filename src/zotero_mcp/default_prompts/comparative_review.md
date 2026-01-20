# Comparative Review Prompt

User request: {papers}

## Step 1: Identify Papers

First, find the papers the user wants to compare:

- If user mentions paper titles/topics → Use `zotero_search_items(query)` to find them
- If user says "recent papers" or "papers I just saved" → Use `zotero_get_recent()`
- If user provides item keys directly → Use those keys
- If unclear → Ask the user which papers to compare

## Step 2: Gather Information

For each paper:
1. Call `zotero_get_item_children(key)` - check for existing review notes
2. If no reviews, use annotations or call `zotero_get_item_fulltext(key)`

## Step 3: Comparative Analysis

Create a synthesis covering these sections. Use tables, bullet points, or prose as appropriate:

- **Executive Summary** - What do these papers collectively reveal?
- **Papers Overview** - Table with authors, year, focus, key innovation
- **Categorization** - Group papers by theme/domain
- **Methods Comparison** - Compare approaches, strengths, limitations
- **Key Findings** - Main results from each paper
- **Consensus** - Where authors agree
- **Conflicts** - Where authors disagree and why
- **Research Evolution** - How the field developed across these papers
- **Challenges & Solutions** - Common problems and proposed solutions
- **Insights** - Recommendations for researchers and practitioners
- **Synthesis** - Overall narrative connecting all papers

### Rules

- Cite specific papers when making claims
- For conflicts, explain WHY authors disagree
- Never fabricate data or citations

## Step 4: Save to Zotero

Ask: "Save this comparative review to Zotero?"

If yes, call `zotero_create_review` with analysis dict and `template_name="comparative_review"`.
