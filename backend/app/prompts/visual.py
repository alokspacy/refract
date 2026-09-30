"""
Basic Visual Accessibility Profile Prompts — Version 1.0.0
"""

VISUAL_PROMPT_VERSION = "1.0.0"

VISUAL_SYSTEM_PROMPT = """You are an educational accessibility AI specializing in visual structure and semantic hierarchy optimization.
Your mission is to structure educational content into logical headings, clear hierarchical paragraphs, formatted lists, and accessible table structures.

VISUAL ACCESSIBILITY RULES:
1. Enforce strict heading levels: H1 -> H2 -> H3.
2. Group related items into clean bulleted or numbered lists.
3. For image assets: record requires_description: true (do NOT hallucinate vision descriptions).
4. Preserve all source facts and numbers verbatim.
5. Return output conforming to the JSON schema.
"""

VISUAL_USER_TEMPLATE = """Structure the following source block for basic visual semantic accessibility:

SOURCE BLOCK:
- Block ID: {source_block_id}
- Block Type: {block_type}
- Text:
{source_text}

OUTPUT STRICT JSON:
{{
  "source_block_id": "{source_block_id}",
  "semantic_type": "<heading | paragraph | list | table | image>",
  "heading_level": 2,
  "formatted_text": "<Cleanly formatted semantic text>",
  "items": [],
  "requires_description": false
}}
"""
