"""
Utility functions for agents
"""
from pathlib import Path


def load_examples_from_md(genre: str) -> str:
    """
    Load story examples from markdown files for a given genre.
    
    Args:
        genre: The genre folder name (e.g., "princess", "christmas", "animals")
        
    Returns:
        Concatenated string of all example stories from the genre folder
    """
    examples_dir = Path(__file__).parent.parent / "examples" / genre
    examples = []
    
    # Load all markdown files from the genre directory
    for file in sorted(examples_dir.glob("*.md")):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            examples.append(f"### Example from {file.stem}:\n{content}\n")
    
    return "\n".join(examples)
