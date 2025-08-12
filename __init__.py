"""
ComfyUI_PromptManager: A comprehensive ComfyUI custom node that extends text encoding 
with persistent prompt storage, advanced search capabilities, and an automatic image 
gallery system.

This module provides two main node types:
- PromptManager: CLIP encoding node that outputs CONDITIONING
- PromptManagerText: Text-only node that outputs STRING with prepend/append functionality

Both nodes share the same database backend for persistent prompt storage and include
an automatic image gallery system that monitors ComfyUI output directories and links
generated images to their source prompts.

Features:
- SQLite-based persistent prompt storage with deduplication
- Advanced search and categorization system  
- Real-time image gallery with metadata extraction
- Web-based admin dashboard for prompt management
- Comprehensive logging and diagnostics
"""

import re
from pathlib import Path


def get_version():
    """Parse version from pyproject.toml"""
    try:
        pyproject_path = Path(__file__).parent / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return "unknown"


from .prompt_manager import PromptManager
from .prompt_manager_text import PromptManagerText

NODE_CLASS_MAPPINGS = {
    "PromptManager": PromptManager,
    "PromptManagerText": PromptManagerText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptManager": "Prompt Manager",
    "PromptManagerText": "Prompt Manager Text",
}

# Define path to web directory for UI components
WEB_DIRECTORY = "web"

# Add API routes (same pattern as ComfyUI_Assets)
try:
    # Set extension URI
    import os

    from .py import config
    from .py.api import PromptManagerAPI

    extension_uri = os.path.dirname(__file__)
    config.extension_uri = extension_uri

    # Register API routes using the same pattern as ComfyUI_Assets
    routes = config.routes
    api = PromptManagerAPI()
    api.add_routes(routes)

except Exception as e:
    # Log to internal logging system without console spam
    try:
        from .utils.logging_config import get_logger

        logger = get_logger("prompt_manager.init")
        logger.error(f"Failed to register API routes: {e}")
    except:
        pass

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

# Print startup message with loaded tools
print()
print(f"\033[94m[ComfyUI-PromptManager] Version:\033[0m {get_version()}")
for node_key, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
    print(f"🫶 \033[94mLoaded:\033[0m {display_name}")
print(f"\033[94mTotal: {len(NODE_CLASS_MAPPINGS)} tools loaded\033[0m")
print()
