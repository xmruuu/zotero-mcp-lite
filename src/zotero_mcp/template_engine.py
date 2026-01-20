"""
Template engine for rendering HTML notes from JSON analysis.

Simple variable substitution using ${variable} syntax.
Metadata is auto-filled from Zotero, analysis content from LLM.
"""

import re
from typing import Any

from zotero_mcp.utils import format_creators, extract_year


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
    # Merge metadata and analysis (metadata takes precedence for conflicts)
    variables = {**analysis, **metadata}
    
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
