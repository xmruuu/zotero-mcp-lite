"""
Configuration management for Zotero MCP.

Handles loading of user-customizable prompt files and HTML templates
from ~/.zotero-mcp/prompts/ directory.
"""

from pathlib import Path


def get_user_config_dir() -> Path:
    """Get the user config directory (~/.zotero-mcp/)."""
    return Path.home() / ".zotero-mcp"


def get_prompts_dir() -> Path:
    """Get the prompts directory (~/.zotero-mcp/prompts/)."""
    return get_user_config_dir() / "prompts"


def load_prompt(name: str) -> str | None:
    """
    Load a prompt file from the prompts directory.
    
    Args:
        name: Prompt name (e.g., "literature_review")
    
    Returns:
        Prompt content string, or None if not found.
    """
    prompt_path = get_prompts_dir() / f"{name}.md"
    
    if prompt_path.exists():
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            pass
    
    return None


def load_template(name: str) -> str | None:
    """
    Load an HTML template file from the prompts directory.
    
    Args:
        name: Template name (e.g., "literature_review")
    
    Returns:
        HTML template string, or None if not found.
    """
    template_path = get_prompts_dir() / f"{name}_template.html"
    
    if template_path.exists():
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            pass
    
    return None


def ensure_prompts_dir() -> Path:
    """
    Ensure the prompts directory exists.
    
    Returns:
        Path to the prompts directory.
    """
    prompts_dir = get_prompts_dir()
    prompts_dir.mkdir(parents=True, exist_ok=True)
    return prompts_dir
