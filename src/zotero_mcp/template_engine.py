"""
Template engine for rendering HTML notes from JSON analysis.

Simple variable substitution using ${variable} syntax.
Metadata is auto-filled from Zotero, analysis content from LLM.
"""

import re
from typing import Any

from zotero_mcp.utils import format_creators, extract_year


# Field aliases: maps common LLM field names to template expected names
FIELD_ALIASES: dict[str, str] = {
    # literature_review template aliases
    "research_problem": "objective",
    "research_objective": "objective",
    "problem": "objective",
    "goal": "objective",
    "research_background": "background",
    "prior_work": "background",
    "related_work": "background",
    "methodology": "methods",
    "method": "methods",
    "approach": "methods",
    "key_findings": "contribution",
    "findings": "contribution",
    "contributions": "contribution",
    "results": "contribution",
    "limitations": "gaps",
    "research_gaps": "gaps",
    "future_directions": "discussion",
    "future_work": "discussion",
    "implications": "discussion",
    "key_quotes": "quotes",
    "important_quotes": "quotes",
    "references_to_read": "to_read",
    "suggested_reading": "to_read",
    "relevance": "discussion",  # merge into discussion if no better fit
    "critical_analysis": "gaps",  # merge into gaps if no better fit
    # comparative_review template aliases
    "executive_summary": "summary",
    "overview": "summary",
    "papers_reviewed": "papers",
    "methods_comparison": "methods",
    "key_findings_comparison": "findings",
    "points_of_consensus": "consensus",
    "agreements": "consensus",
    "conflicts_debates": "conflicts",
    "debates": "conflicts",
    "disagreements": "conflicts",
    "research_evolution": "evolution",
    "timeline": "evolution",
    "challenges_solutions": "challenges",
    "recommendations": "insights",
    "takeaways": "insights",
    "overall_synthesis": "synthesis",
    "conclusion": "synthesis",
}


def normalize_analysis_fields(analysis: dict[str, str]) -> dict[str, str]:
    """
    Normalize analysis field names using aliases.
    
    Maps common LLM field names to template expected names.
    Preserves original fields that don't have aliases.
    """
    normalized = {}
    for key, value in analysis.items():
        # Use alias if exists, otherwise keep original
        normalized_key = FIELD_ALIASES.get(key.lower(), key)
        # Don't overwrite if already set (first value wins)
        if normalized_key not in normalized:
            normalized[normalized_key] = value
    return normalized


def render_review(template: str, metadata: dict[str, str], analysis: dict[str, str]) -> str:
    """
    Render an HTML template with metadata and analysis content.
    
    Args:
        template: HTML template string with ${variable} placeholders
        metadata: Dict with Zotero metadata (title, authors, year, etc.)
        analysis: Dict with LLM analysis content (contribution, gaps, etc.)
    
    Returns:
        Rendered HTML string
    """
    # Normalize analysis field names (handle LLM variations)
    normalized_analysis = normalize_analysis_fields(analysis)
    
    # Merge metadata and analysis (metadata takes precedence for conflicts)
    variables = {**normalized_analysis, **metadata}
    
    def replace_var(match: re.Match) -> str:
        var_name = match.group(1)
        value = variables.get(var_name, "")
        if value is None:
            return ""
        return str(value)
    
    # Replace ${variable} patterns
    return re.sub(r'\$\{(\w+)\}', replace_var, template)


def build_metadata_dict(item: dict) -> dict[str, str]:
    """
    Extract metadata from a Zotero item for template rendering.
    
    Args:
        item: Zotero item dictionary from API
    
    Returns:
        Dictionary with standard metadata fields:
        - title, authors, year, publicationTitle, DOI, abstractNote, tags, itemLink
    """
    data = item.get("data", {})
    
    # Format authors
    creators = data.get("creators", [])
    authors = format_creators(creators)
    
    # Extract year from date
    date = data.get("date", "")
    year = extract_year(date)
    
    # Build tags string
    tags = data.get("tags", [])
    tags_str = ", ".join(t.get("tag", "") for t in tags) if tags else ""
    
    # Build Zotero item link
    item_key = item.get("key", "")
    item_link = f"zotero://select/library/items/{item_key}" if item_key else ""
    
    return {
        "title": data.get("title", "Untitled"),
        "authors": authors,
        "year": year,
        "publicationTitle": data.get("publicationTitle", ""),
        "DOI": data.get("DOI", ""),
        "abstractNote": data.get("abstractNote", ""),
        "tags": tags_str,
        "itemLink": item_link,
        "itemKey": item_key,
    }
