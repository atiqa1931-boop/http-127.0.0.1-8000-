import re

def preprocess_text(text: str) -> str:
    """
    Pipeline 2: Cleans raw text data before tokenization.
    - Normalizes diverse quotes (“ ” ‘ ’) to standard straight quotes.
    - Consolidates multiple spaces or tabs into a single space.
    - Crucially, it preserves raw capitalization because structural noun 
      detection (Pipeline 4) depends heavily on capitalization patterns.
    """
    if not text:
        return ""
    
    # 1. Normalize typographic smart quotes to straight variants
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("`", "'")
    
    # 2. Normalize horizontal whitespace (spaces/tabs) without removing structural newlines (\n)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()
